"""Backup manager simplificado utilizadas pelos testes.
Ele trabalha apenas com bancos SQLite locais e armazena backups em
<repo>/backups.
"""
from __future__ import annotations

import os
import shutil
from datetime import datetime
from typing import List, Dict, Any
import logging

logger = logging.getLogger(__name__)

_BACKUP_DIR = "backups"

# Garante diretório
os.makedirs(_BACKUP_DIR, exist_ok=True)


class _BackupManager:
    """Gerencia backups do banco de dados (stub)."""

    def __init__(self) -> None:
        try:
            from app.db.database import db_manager  # noqa: WPS433
        except ImportError as error:  # pragma: no cover
            logger.error("BackupManager requer db_manager: %s", error)
            raise
        self._db_manager = db_manager

    # ------------------------------------------------------------------
    def create_database_backup(self) -> str | None:
        """Cria um backup simples do arquivo SQLite.
        Para bancos não SQLite retorna None.
        """
        db_url = self._db_manager.database_url
        if not db_url.startswith("sqlite"):
            logger.warning("Backup automático não implementado para %s", db_url)
            return None

        # Caminho do arquivo SQLite
        db_path = db_url.replace("sqlite:///", "")
        if not os.path.exists(db_path):
            logger.warning("Arquivo de banco de dados não encontrado: %s", db_path)
            return None

        ts = datetime.now().strftime("%Y%m%d_%H%M%S")
        backup_name = f"backup_{ts}.db"
        backup_path = os.path.join(_BACKUP_DIR, backup_name)
        try:
            shutil.copy2(db_path, backup_path)
            logger.info("Backup criado: %s", backup_path)
            return backup_path
        except Exception as exc:  # noqa: BLE001
            logger.exception("Falha ao criar backup: %s", exc)
            return None

    # ------------------------------------------------------------------
    def list_backups(self) -> List[str]:
        """Lista arquivos de backup disponíveis."""
        backups = [f for f in os.listdir(_BACKUP_DIR) if f.endswith(".db")]
        backups.sort(reverse=True)
        return [os.path.join(_BACKUP_DIR, b) for b in backups]

    # ------------------------------------------------------------------
    def get_backup_status(self) -> Dict[str, Any]:
        backups = self.list_backups()
        return {
            "total_backups": len(backups),
            "latest_backup": backups[0] if backups else None,
            "backup_dir": os.path.abspath(_BACKUP_DIR),
        }


backup_manager = _BackupManager()