import shutil
import threading
import time
import zipfile
from datetime import datetime, timedelta
from pathlib import Path
from typing import Any, Dict, Optional

import boto3
import schedule

from app.core.config import settings
from app.core.logger import get_logger, log_performance_metric

logger = get_logger(__name__)

class BackupManager:
    """Gerenciador de backup automático"""

    def __init__(self):
        self.backup_dir = Path("backups")
        self.backup_dir.mkdir(exist_ok=True)

        # Configurações de backup
        self.backup_config = {
            "database": {
                "enabled": True,
                "frequency": "daily",  # daily, weekly, monthly
                "retention_days": 30,
                "compress": True
            },
            "files": {
                "enabled": True,
                "frequency": "weekly",
                "retention_days": 90,
                "include_patterns": ["*.json", "*.log", "*.db"],
                "exclude_patterns": ["*.tmp", "*.cache", "__pycache__"]
            },
            "cloud": {
                "enabled": False,
                "provider": "s3",  # s3, gcs, azure
                "bucket": None,
                "region": None,
                "encryption": True
            }
        }

        # Configurar AWS S3 se disponível
        self.s3_client = None
        if settings.AWS_ACCESS_KEY_ID and settings.AWS_SECRET_ACCESS_KEY:
            try:
                self.s3_client = boto3.client(
                    's3',
                    aws_access_key_id=settings.AWS_ACCESS_KEY_ID,
                    aws_secret_access_key=settings.AWS_SECRET_ACCESS_KEY,
                    region_name=settings.AWS_REGION or 'us-east-1'
                )
                logger.info("AWS S3 client configured for backup")
            except Exception as e:
                logger.warning(f"Failed to configure AWS S3: {e}")

        # Histórico de backups
        self.backup_history = []

        # Iniciar scheduler em thread separada
        self._start_scheduler()

    def _start_scheduler(self):
        """Inicia o scheduler de backup em thread separada"""

        def run_scheduler():
            # Agendar backups
            if self.backup_config["database"]["enabled"]:
                if self.backup_config["database"]["frequency"] == "daily":
                    schedule.every().day.at("02:00").do(self.create_database_backup)
                elif self.backup_config["database"]["frequency"] == "weekly":
                    schedule.every().sunday.at("02:00").do(self.create_database_backup)
                elif self.backup_config["database"]["frequency"] == "monthly":
                    schedule.every().month.at("02:00").do(self.create_database_backup)

            if self.backup_config["files"]["enabled"]:
                if self.backup_config["files"]["frequency"] == "daily":
                    schedule.every().day.at("03:00").do(self.create_files_backup)
                elif self.backup_config["files"]["frequency"] == "weekly":
                    schedule.every().sunday.at("03:00").do(self.create_files_backup)
                elif self.backup_config["files"]["frequency"] == "monthly":
                    schedule.every().month.at("03:00").do(self.create_files_backup)

            # Executar limpeza diária
            schedule.every().day.at("04:00").do(self.cleanup_old_backups)

            # Loop do scheduler
            while True:
                schedule.run_pending()
                time.sleep(60)  # Verificar a cada minuto

        # Iniciar thread
        scheduler_thread = threading.Thread(target=run_scheduler, daemon=True)
        scheduler_thread.start()
        logger.info("Backup scheduler started")

    def create_database_backup(self) -> Dict[str, Any]:
        """Cria backup do banco de dados"""

        try:
            start_time = time.time()
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")

            # Caminho do banco de dados
            db_path = Path(settings.DATABASE_URL.replace("sqlite:///", ""))
            if not db_path.exists():
                raise FileNotFoundError(f"Database file not found: {db_path}")

            # Nome do arquivo de backup
            backup_filename = f"database_backup_{timestamp}.db"
            backup_path = self.backup_dir / backup_filename

            # Copiar banco de dados
            shutil.copy2(db_path, backup_path)

            # Comprimir se habilitado
            if self.backup_config["database"]["compress"]:
                compressed_path = backup_path.with_suffix('.db.zip')
                with zipfile.ZipFile(
                    compressed_path, 'w', zipfile.ZIP_DEFLATED
                ) as zipf:
                    zipf.write(backup_path, backup_filename)

                # Remover arquivo não comprimido
                backup_path.unlink()
                backup_path = compressed_path

            # Upload para nuvem se habilitado
            cloud_url = None
            if self.backup_config["cloud"]["enabled"] and self.s3_client:
                cloud_url = self._upload_to_cloud(backup_path, "database")

            duration = time.time() - start_time
            file_size = backup_path.stat().st_size

            # Registrar backup
            backup_info = {
                "type": "database",
                "filename": backup_path.name,
                "path": str(backup_path),
                "size_bytes": file_size,
                "size_mb": round(file_size / (1024 * 1024), 2),
                "timestamp": timestamp,
                "created_at": datetime.now().isoformat(),
                "duration_seconds": round(duration, 2),
                "cloud_url": cloud_url,
                "success": True
            }

            self.backup_history.append(backup_info)

            # Log de performance
            log_performance_metric(
                logger,
                "database_backup",
                duration,
                "seconds",
                f"Size: {backup_info['size_mb']}MB"
            )

            logger.info(
                f"Database backup created: {backup_path.name} "
                f"({backup_info['size_mb']}MB)"
            )

            return backup_info

        except Exception as e:
            logger.error(f"Error creating database backup: {e}")
            return {
                "type": "database",
                "success": False,
                "error": str(e),
                "timestamp": datetime.now().isoformat()
            }

    def create_files_backup(self) -> Dict[str, Any]:
        """Cria backup de arquivos"""

        try:
            start_time = time.time()
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")

            # Nome do arquivo de backup
            backup_filename = f"files_backup_{timestamp}.zip"
            backup_path = self.backup_dir / backup_filename

            # Criar arquivo ZIP
            with zipfile.ZipFile(backup_path, 'w', zipfile.ZIP_DEFLATED) as zipf:
                # Adicionar arquivos baseado nos padrões
                for pattern in self.backup_config["files"]["include_patterns"]:
                    for file_path in Path(".").rglob(pattern):
                        # Verificar se deve ser excluído
                        if self._should_exclude_file(file_path):
                            continue

                        # Adicionar ao ZIP
                        zipf.write(file_path, file_path.relative_to(Path(".")))

            # Upload para nuvem se habilitado
            cloud_url = None
            if self.backup_config["cloud"]["enabled"] and self.s3_client:
                cloud_url = self._upload_to_cloud(backup_path, "files")

            duration = time.time() - start_time
            file_size = backup_path.stat().st_size

            # Registrar backup
            backup_info = {
                "type": "files",
                "filename": backup_path.name,
                "path": str(backup_path),
                "size_bytes": file_size,
                "size_mb": round(file_size / (1024 * 1024), 2),
                "timestamp": timestamp,
                "created_at": datetime.now().isoformat(),
                "duration_seconds": round(duration, 2),
                "cloud_url": cloud_url,
                "success": True
            }

            self.backup_history.append(backup_info)

            # Log de performance
            log_performance_metric(
                logger,
                "files_backup",
                duration,
                "seconds",
                f"Size: {backup_info['size_mb']}MB"
            )

            logger.info(
                f"Files backup created: {backup_path.name} "
                f"({backup_info['size_mb']}MB)"
            )

            return backup_info

        except Exception as e:
            logger.error(f"Error creating files backup: {e}")
            return {
                "type": "files",
                "success": False,
                "error": str(e),
                "timestamp": datetime.now().isoformat()
            }

    def _should_exclude_file(self, file_path: Path) -> bool:
        """Verifica se arquivo deve ser excluído do backup"""

        for pattern in self.backup_config["files"]["exclude_patterns"]:
            if pattern in str(file_path):
                return True

        # Excluir arquivos muito grandes (>100MB)
        if file_path.stat().st_size > 100 * 1024 * 1024:
            return True

        return False

    def _upload_to_cloud(self, file_path: Path, backup_type: str) -> Optional[str]:
        """Faz upload do backup para a nuvem"""

        try:
            if not self.s3_client or not settings.AWS_S3_BUCKET:
                return None

            # Nome do objeto no S3
            s3_key = f"backups/{backup_type}/{file_path.name}"

            # Upload com criptografia se habilitada
            extra_args = {}
            if self.backup_config["cloud"]["encryption"]:
                extra_args['ServerSideEncryption'] = 'AES256'

            self.s3_client.upload_file(
                str(file_path),
                settings.AWS_S3_BUCKET,
                s3_key,
                ExtraArgs=extra_args
            )

            # URL do objeto
            cloud_url = f"s3://{settings.AWS_S3_BUCKET}/{s3_key}"

            logger.info(f"Backup uploaded to cloud: {cloud_url}")
            return cloud_url

        except Exception as e:
            logger.error(f"Error uploading to cloud: {e}")
            return None

    def cleanup_old_backups(self) -> Dict[str, Any]:
        """Remove backups antigos baseado na política de retenção"""

        try:
            deleted_count = 0
            freed_space = 0

            # Limpar backups de banco de dados
            if self.backup_config["database"]["enabled"]:
                retention_days = self.backup_config["database"]["retention_days"]
                cutoff_date = datetime.now() - timedelta(days=retention_days)

                for backup_file in self.backup_dir.glob("database_backup_*"):
                    if self._is_file_older_than(backup_file, cutoff_date):
                        file_size = backup_file.stat().st_size
                        backup_file.unlink()
                        deleted_count += 1
                        freed_space += file_size
                        logger.info(f"Deleted old database backup: {backup_file.name}")

            # Limpar backups de arquivos
            if self.backup_config["files"]["enabled"]:
                retention_days = self.backup_config["files"]["retention_days"]
                cutoff_date = datetime.now() - timedelta(days=retention_days)

                for backup_file in self.backup_dir.glob("files_backup_*"):
                    if self._is_file_older_than(backup_file, cutoff_date):
                        file_size = backup_file.stat().st_size
                        backup_file.unlink()
                        deleted_count += 1
                        freed_space += file_size
                        logger.info(f"Deleted old files backup: {backup_file.name}")

            # Limpar da nuvem se habilitado
            if self.backup_config["cloud"]["enabled"] and self.s3_client:
                self._cleanup_cloud_backups()

            freed_space_mb = round(freed_space / (1024 * 1024), 2)

            logger.info(
                f"Cleanup completed: {deleted_count} files deleted, "
                f"{freed_space_mb}MB freed"
            )

            return {
                "deleted_count": deleted_count,
                "freed_space_bytes": freed_space,
                "freed_space_mb": freed_space_mb,
                "success": True
            }

        except Exception as e:
            logger.error(f"Error during cleanup: {e}")
            return {
                "success": False,
                "error": str(e)
            }

    def _is_file_older_than(self, file_path: Path, cutoff_date: datetime) -> bool:
        """Verifica se arquivo é mais antigo que a data especificada"""

        try:
            # Tentar extrair data do nome do arquivo
            filename = file_path.stem
            if "_" in filename:
                date_str = filename.split("_")[-2] + "_" + filename.split("_")[-1]
                file_date = datetime.strptime(date_str, "%Y%m%d_%H%M%S")
                return file_date < cutoff_date
        except (ValueError, IndexError):
            pass

        # Fallback: usar data de modificação
        file_mtime = datetime.fromtimestamp(file_path.stat().st_mtime)
        return file_mtime < cutoff_date

    def _cleanup_cloud_backups(self):
        """Remove backups antigos da nuvem"""

        try:
            if not self.s3_client or not settings.AWS_S3_BUCKET:
                return

            # Listar objetos no bucket
            response = self.s3_client.list_objects_v2(
                Bucket=settings.AWS_S3_BUCKET,
                Prefix="backups/"
            )

            if 'Contents' not in response:
                return

            # Calcular data de corte
            retention_days = max(
                self.backup_config["database"]["retention_days"],
                self.backup_config["files"]["retention_days"]
            )
            cutoff_date = datetime.now() - timedelta(days=retention_days)

            # Deletar objetos antigos
            for obj in response['Contents']:
                if obj['LastModified'].replace(tzinfo=None) < cutoff_date:
                    self.s3_client.delete_object(
                        Bucket=settings.AWS_S3_BUCKET,
                        Key=obj['Key']
                    )
                    logger.info(f"Deleted old cloud backup: {obj['Key']}")

        except Exception as e:
            logger.error(f"Error cleaning up cloud backups: {e}")

    def get_backup_status(self) -> Dict[str, Any]:
        """Obtém status dos backups"""

        # Estatísticas dos backups
        total_backups = len(self.backup_history)
        successful_backups = len([b for b in self.backup_history if b.get("success", False)])
        failed_backups = total_backups - successful_backups

        # Tamanho total dos backups
        total_size = sum(b.get("size_bytes", 0) for b in self.backup_history)
        total_size_mb = round(total_size / (1024 * 1024), 2)

        # Últimos backups
        recent_backups = sorted(
            self.backup_history,
            key=lambda x: x.get("created_at", ""),
            reverse=True
        )[:5]

        # Espaço em disco
        backup_dir_size = sum(
            f.stat().st_size for f in self.backup_dir.rglob("*") if f.is_file()
        )
        backup_dir_size_mb = round(backup_dir_size / (1024 * 1024), 2)

        return {
            "total_backups": total_backups,
            "successful_backups": successful_backups,
            "failed_backups": failed_backups,
            "success_rate": (
                round(successful_backups / total_backups * 100, 2)
                if total_backups > 0
                else 0
            ),
            "total_size_mb": total_size_mb,
            "backup_dir_size_mb": backup_dir_size_mb,
            "recent_backups": recent_backups,
            "config": self.backup_config
        }

    def restore_database_backup(self, backup_filename: str) -> Dict[str, Any]:
        """Restaura backup do banco de dados"""

        try:
            backup_path = self.backup_dir / backup_filename

            if not backup_path.exists():
                raise FileNotFoundError(f"Backup file not found: {backup_filename}")

            # Verificar se é um arquivo comprimido
            if backup_path.suffix == '.zip':
                # Extrair arquivo
                with zipfile.ZipFile(backup_path, 'r') as zipf:
                    db_filename = [f for f in zipf.namelist() if f.endswith('.db')][0]
                    zipf.extract(db_filename, self.backup_dir)
                    extracted_path = self.backup_dir / db_filename
            else:
                extracted_path = backup_path

            # Fazer backup do banco atual
            current_db_path = Path(settings.DATABASE_URL.replace("sqlite:///", ""))
            if current_db_path.exists():
                timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
                current_backup = (
                    current_db_path.parent / f"pre_restore_backup_{timestamp}.db"
                )
                shutil.copy2(current_db_path, current_backup)

            # Restaurar backup
            shutil.copy2(extracted_path, current_db_path)

            # Limpar arquivo extraído se necessário
            if extracted_path != backup_path:
                extracted_path.unlink()

            logger.info(f"Database restored from backup: {backup_filename}")

            return {
                "success": True,
                "message": f"Database restored from {backup_filename}",
                "backup_file": backup_filename
            }

        except Exception as e:
            logger.error(f"Error restoring database backup: {e}")
            return {
                "success": False,
                "error": str(e)
            }

# Instância global
backup_manager = BackupManager()

# Funções utilitárias
def create_manual_backup(backup_type: str = "both") -> Dict[str, Any]:
    """Cria backup manual"""

    if backup_type == "database":
        return backup_manager.create_database_backup()
    elif backup_type == "files":
        return backup_manager.create_files_backup()
    elif backup_type == "both":
        db_result = backup_manager.create_database_backup()
        files_result = backup_manager.create_files_backup()
        return {
            "database": db_result,
            "files": files_result
        }
    else:
        raise ValueError("backup_type must be 'database', 'files', or 'both'")

def get_backup_status() -> Dict[str, Any]:
    """Obtém status dos backups"""
    return backup_manager.get_backup_status()

def cleanup_old_backups() -> Dict[str, Any]:
    """Remove backups antigos"""
    return backup_manager.cleanup_old_backups()
