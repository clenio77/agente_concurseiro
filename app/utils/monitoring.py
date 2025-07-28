import sqlite3
import threading
import time
from collections import defaultdict, deque
from datetime import datetime, timedelta
from pathlib import Path
from typing import Any, Dict, List

import psutil

from app.core.config import settings
from app.core.logger import get_logger, log_performance_metric

logger = get_logger(__name__)

class SystemMonitor:
    """Monitor de sistema e performance"""

    def __init__(self):
        self.metrics_history = defaultdict(
            lambda: deque(maxlen=1000)
        )  # Últimas 1000 medições
        self.alerts = []
        self.thresholds = {
            "cpu_percent": 80.0,
            "memory_percent": 85.0,
            "disk_percent": 90.0,
            "response_time_ms": 5000,  # 5 segundos
            "error_rate": 5.0,  # 5%
            "active_connections": 100
        }

        # Estatísticas em tempo real
        self.stats = {
            "start_time": datetime.now(),
            "total_requests": 0,
            "successful_requests": 0,
            "failed_requests": 0,
            "total_response_time": 0,
            "peak_memory_usage": 0,
            "peak_cpu_usage": 0
        }

        # Iniciar monitoramento em background
        self.monitoring_active = True
        self._start_monitoring()

    def _start_monitoring(self):
        """Inicia monitoramento em thread separada"""

        def monitor_loop():
            while self.monitoring_active:
                try:
                    # Coletar métricas do sistema
                    metrics = self._collect_system_metrics()

                    # Armazenar métricas
                    for key, value in metrics.items():
                        self.metrics_history[key].append({
                            "timestamp": datetime.now().isoformat(),
                            "value": value
                        })

                    # Verificar alertas
                    self._check_alerts(metrics)

                    # Atualizar estatísticas
                    self._update_stats(metrics)

                    # Aguardar próxima medição
                    time.sleep(60)  # Medir a cada minuto

                except Exception as e:
                    logger.error(f"Error in monitoring loop: {e}")
                    time.sleep(60)

        # Iniciar thread
        monitor_thread = threading.Thread(target=monitor_loop, daemon=True)
        monitor_thread.start()
        logger.info("System monitoring started")

    def _collect_system_metrics(self) -> Dict[str, float]:
        """Coleta métricas do sistema"""

        try:
            # CPU
            cpu_percent = psutil.cpu_percent(interval=1)

            # Memória
            memory = psutil.virtual_memory()
            memory_percent = memory.percent
            memory_used_mb = memory.used / (1024 * 1024)
            memory_total_mb = memory.total / (1024 * 1024)

            # Disco
            disk = psutil.disk_usage('/')
            disk_percent = disk.percent
            disk_used_gb = disk.used / (1024 * 1024 * 1024)
            disk_total_gb = disk.total / (1024 * 1024 * 1024)

            # Rede
            network = psutil.net_io_counters()
            network_bytes_sent = network.bytes_sent
            network_bytes_recv = network.bytes_recv

            # Processos
            process = psutil.Process()
            process_cpu_percent = process.cpu_percent()
            process_memory_mb = process.memory_info().rss / (1024 * 1024)

            # Conexões de rede
            connections = len(psutil.net_connections())

            # Uptime
            uptime_seconds = time.time() - psutil.boot_time()

            return {
                "cpu_percent": cpu_percent,
                "memory_percent": memory_percent,
                "memory_used_mb": memory_used_mb,
                "memory_total_mb": memory_total_mb,
                "disk_percent": disk_percent,
                "disk_used_gb": disk_used_gb,
                "disk_total_gb": disk_total_gb,
                "network_bytes_sent": network_bytes_sent,
                "network_bytes_recv": network_bytes_recv,
                "process_cpu_percent": process_cpu_percent,
                "process_memory_mb": process_memory_mb,
                "connections": connections,
                "uptime_seconds": uptime_seconds
            }

        except Exception as e:
            logger.error(f"Error collecting system metrics: {e}")
            return {}

    def _check_alerts(self, metrics: Dict[str, float]):
        """Verifica se há alertas baseado nas métricas"""

        for metric, value in metrics.items():
            if metric in self.thresholds:
                threshold = self.thresholds[metric]

                if value > threshold:
                    alert = {
                        "timestamp": datetime.now().isoformat(),
                        "metric": metric,
                        "value": value,
                        "threshold": threshold,
                        "severity": "high" if value > threshold * 1.5 else "medium"
                    }

                    self.alerts.append(alert)

                    # Log do alerta
                    logger.warning(
                        f"System alert: {metric} = {value} (threshold: {threshold})",
                        extra={
                            "alert": alert,
                            "operation": f"MONITORING:ALERT:{metric}"
                        }
                    )

    def _update_stats(self, metrics: Dict[str, float]):
        """Atualiza estatísticas em tempo real"""

        # Atualizar picos
        if metrics.get("memory_percent", 0) > self.stats["peak_memory_usage"]:
            self.stats["peak_memory_usage"] = metrics["memory_percent"]

        if metrics.get("cpu_percent", 0) > self.stats["peak_cpu_usage"]:
            self.stats["peak_cpu_usage"] = metrics["cpu_percent"]

    def record_request(
        self, method: str, path: str, status_code: int, duration_ms: float
    ):
        """Registra uma requisição HTTP"""

        self.stats["total_requests"] += 1
        self.stats["total_response_time"] += duration_ms

        if 200 <= status_code < 400:
            self.stats["successful_requests"] += 1
        else:
            self.stats["failed_requests"] += 1

        # Log de performance
        log_performance_metric(
            logger,
            "http_request",
            duration_ms / 1000,  # Converter para segundos
            "seconds",
            f"{method} {path} - {status_code}"
        )

    def get_system_status(self) -> Dict[str, Any]:
        """Obtém status atual do sistema"""

        current_metrics = self._collect_system_metrics()

        # Calcular taxas
        total_requests = self.stats["total_requests"]
        success_rate = 0
        avg_response_time = 0

        if total_requests > 0:
            success_rate = (self.stats["successful_requests"] / total_requests) * 100
            avg_response_time = self.stats["total_response_time"] / total_requests

        # Status geral
        system_status = "healthy"
        if current_metrics.get("cpu_percent", 0) > self.thresholds["cpu_percent"]:
            system_status = "warning"
        if current_metrics.get("memory_percent", 0) > self.thresholds["memory_percent"]:
            system_status = "critical"

        return {
            "status": system_status,
            "uptime": {
                "seconds": current_metrics.get("uptime_seconds", 0),
                "formatted": str(
                    timedelta(seconds=int(current_metrics.get("uptime_seconds", 0)))
                )
            },
            "performance": {
                "cpu_percent": current_metrics.get("cpu_percent", 0),
                "memory_percent": current_metrics.get("memory_percent", 0),
                "disk_percent": current_metrics.get("disk_percent", 0),
                "process_memory_mb": current_metrics.get("process_memory_mb", 0)
            },
            "requests": {
                "total": total_requests,
                "successful": self.stats["successful_requests"],
                "failed": self.stats["failed_requests"],
                "success_rate": round(success_rate, 2),
                "avg_response_time_ms": round(avg_response_time, 2)
            },
            "peaks": {
                "peak_cpu_usage": self.stats["peak_cpu_usage"],
                "peak_memory_usage": self.stats["peak_memory_usage"]
            },
            "alerts": {
                "total": len(self.alerts),
                "recent": self.alerts[-10:] if self.alerts else []
            }
        }

    def get_metrics_history(self, metric: str, hours: int = 24) -> List[Dict[str, Any]]:
        """Obtém histórico de métricas"""

        if metric not in self.metrics_history:
            return []

        cutoff_time = datetime.now() - timedelta(hours=hours)
        history = []

        for entry in self.metrics_history[metric]:
            entry_time = datetime.fromisoformat(entry["timestamp"])
            if entry_time >= cutoff_time:
                history.append(entry)

        return history

    def get_performance_report(self) -> Dict[str, Any]:
        """Gera relatório de performance"""

        # Estatísticas das últimas 24 horas
        cpu_history = self.get_metrics_history("cpu_percent", 24)
        memory_history = self.get_metrics_history("memory_percent", 24)

        # Calcular médias
        avg_cpu = (
            sum(entry["value"] for entry in cpu_history) / len(cpu_history)
            if cpu_history
            else 0
        )
        avg_memory = (
            sum(entry["value"] for entry in memory_history) / len(memory_history)
            if memory_history
            else 0
        )

        # Calcular picos
        max_cpu = max(entry["value"] for entry in cpu_history) if cpu_history else 0
        max_memory = (
            max(entry["value"] for entry in memory_history) if memory_history else 0
        )

        # Taxa de erro
        total_requests = self.stats["total_requests"]
        error_rate = (
            (self.stats["failed_requests"] / total_requests * 100)
            if total_requests > 0
            else 0
        )

        return {
            "period": "24h",
            "generated_at": datetime.now().isoformat(),
            "averages": {
                "cpu_percent": round(avg_cpu, 2),
                "memory_percent": round(avg_memory, 2)
            },
            "peaks": {
                "cpu_percent": round(max_cpu, 2),
                "memory_percent": round(max_memory, 2)
            },
            "requests": {
                "total": total_requests,
                "success_rate": (
                    round(
                        (self.stats["successful_requests"] / total_requests * 100),
                        2
                    )
                    if total_requests > 0
                    else 0
                ),
                "error_rate": round(error_rate, 2),
                "avg_response_time_ms": (
                    round(self.stats["total_response_time"] / total_requests, 2)
                    if total_requests > 0
                    else 0
                )
            },
            "alerts": {
                "total": len(self.alerts),
                "critical": len([a for a in self.alerts if a["severity"] == "critical"]),
                "medium": len([a for a in self.alerts if a["severity"] == "medium"])
            }
        }

    def set_threshold(self, metric: str, value: float):
        """Define threshold para uma métrica"""

        if metric in self.thresholds:
            self.thresholds[metric] = value
            logger.info(f"Threshold updated for {metric}: {value}")
        else:
            raise ValueError(f"Unknown metric: {metric}")

    def clear_alerts(self):
        """Limpa alertas antigos"""

        # Manter apenas alertas das últimas 24 horas
        cutoff_time = datetime.now() - timedelta(hours=24)
        self.alerts = [
            alert for alert in self.alerts
            if datetime.fromisoformat(alert["timestamp"]) >= cutoff_time
        ]

        logger.info(f"Cleared old alerts, {len(self.alerts)} remaining")

class DatabaseMonitor:
    """Monitor específico para banco de dados"""

    def __init__(self, db_path: str):
        self.db_path = db_path

    def get_database_stats(self) -> Dict[str, Any]:
        """Obtém estatísticas do banco de dados"""

        try:
            # Conectar ao banco
            conn = sqlite3.connect(self.db_path)
            cursor = conn.cursor()

            # Tamanho do arquivo
            file_size = Path(self.db_path).stat().st_size
            file_size_mb = file_size / (1024 * 1024)

            # Número de tabelas
            cursor.execute("SELECT name FROM sqlite_master WHERE type='table'")
            tables = cursor.fetchall()
            num_tables = len(tables)

            # Estatísticas por tabela
            table_stats = {}
            total_rows = 0

            for table in tables:
                table_name = table[0]
                cursor.execute(f"SELECT COUNT(*) FROM {table_name}")
                row_count = cursor.fetchone()[0]
                table_stats[table_name] = row_count
                total_rows += row_count

            # Informações de integridade
            cursor.execute("PRAGMA integrity_check")
            integrity_check = cursor.fetchone()[0]

            # Configurações do SQLite
            cursor.execute("PRAGMA page_count")
            page_count = cursor.fetchone()[0]

            cursor.execute("PRAGMA page_size")
            page_size = cursor.fetchone()[0]

            # Tamanho estimado do banco
            estimated_size = page_count * page_size

            conn.close()

            return {
                "file_size_mb": round(file_size_mb, 2),
                "estimated_size_mb": round(estimated_size / (1024 * 1024), 2),
                "num_tables": num_tables,
                "total_rows": total_rows,
                "table_stats": table_stats,
                "integrity_check": integrity_check,
                "page_count": page_count,
                "page_size": page_size
            }

        except Exception as e:
            logger.error(f"Error getting database stats: {e}")
            return {
                "error": str(e)
            }

    def optimize_database(self) -> Dict[str, Any]:
        """Otimiza o banco de dados"""

        try:
            conn = sqlite3.connect(self.db_path)
            cursor = conn.cursor()

            # Executar VACUUM para otimizar
            cursor.execute("VACUUM")

            # Executar ANALYZE para atualizar estatísticas
            cursor.execute("ANALYZE")

            # Reindexar
            cursor.execute("REINDEX")

            conn.close()

            logger.info("Database optimization completed")

            return {
                "success": True,
                "message": "Database optimization completed"
            }

        except Exception as e:
            logger.error(f"Error optimizing database: {e}")
            return {
                "success": False,
                "error": str(e)
            }

# Instâncias globais
system_monitor = SystemMonitor()
database_monitor = DatabaseMonitor(settings.DATABASE_URL.replace("sqlite:///", ""))

# Funções utilitárias
def get_system_status() -> Dict[str, Any]:
    """Obtém status do sistema"""
    return system_monitor.get_system_status()

def get_performance_report() -> Dict[str, Any]:
    """Obtém relatório de performance"""
    return system_monitor.get_performance_report()

def get_database_stats() -> Dict[str, Any]:
    """Obtém estatísticas do banco de dados"""
    return database_monitor.get_database_stats()

def record_request(method: str, path: str, status_code: int, duration_ms: float):
    """Registra uma requisição HTTP"""
    system_monitor.record_request(method, path, status_code, duration_ms)

def optimize_database() -> Dict[str, Any]:
    """Otimiza o banco de dados"""
    return database_monitor.optimize_database()
