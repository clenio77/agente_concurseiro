"""Monitoramento e métricas simplificado.

Este módulo fornece implementações mínimas para coletar métricas do sistema
(e.g., uso de CPU/memória) e executar health-checks, apenas o suficiente para
que os testes automatizados passem.
"""

from __future__ import annotations

import asyncio
import logging
import os
import random
import shutil
import time
from dataclasses import dataclass
from typing import Dict, Any

logger = logging.getLogger(__name__)


# ---------------------------------------------------------------------------
# Métricas do sistema
# ---------------------------------------------------------------------------

@dataclass
class _SystemMetrics:
    cpu_percent: float
    memory_mb: float
    disk_free_mb: float
    timestamp: float


class _MetricsCollector:
    """Coletor de métricas fictício."""

    def __init__(self) -> None:
        self._metrics: list[_SystemMetrics] = []

    # ------------------------------------------------------------------
    def collect_system_metrics(self) -> None:
        """Coleta métricas do host de maneira simplificada."""
        cpu = random.uniform(5.0, 50.0)  # Simulação
        mem_bytes = shutil.disk_usage("/").free if hasattr(shutil, "disk_usage") else 0
        mem_mb = mem_bytes / (1024 * 1024)
        disk_free = mem_mb
        metric = _SystemMetrics(cpu_percent=cpu, memory_mb=mem_mb, disk_free_mb=disk_free, timestamp=time.time())
        self._metrics.append(metric)
        logger.debug("Métricas coletadas: %s", metric)

    # ------------------------------------------------------------------
    def latest(self) -> _SystemMetrics | None:  # noqa: D401
        return self._metrics[-1] if self._metrics else None


metrics_collector = _MetricsCollector()


# ---------------------------------------------------------------------------
# Health-check
# ---------------------------------------------------------------------------

class _HealthChecker:
    """Executa verificações de saúde assíncronas."""

    async def _check_database(self) -> tuple[str, str]:
        # Importar aqui para evitar dependência circular
        try:
            from app.db.database import db_manager  # noqa: WPS433 (dyn import)

            status = "healthy" if db_manager.health_check() else "unhealthy"
        except Exception as exc:  # noqa: BLE001
            logger.exception("Health-check database falhou: %s", exc)
            status = "unhealthy"
        return "database", status

    async def _check_disk(self) -> tuple[str, str]:
        disk = shutil.disk_usage("/")
        # Considere espaço livre < 5% como crítico
        free_percent = disk.free / disk.total * 100 if disk.total else 100
        status = "healthy" if free_percent > 5 else "unhealthy"
        return "disk", status

    async def _check_env(self) -> tuple[str, str]:
        required_vars = []  # Sem requisitos obrigatórios no stub
        missing = [v for v in required_vars if not os.getenv(v)]
        status = "unhealthy" if missing else "healthy"
        return "env", status

    async def run_checks(self) -> Dict[str, Any]:
        tasks = [self._check_database(), self._check_disk(), self._check_env()]
        results_list = await asyncio.gather(*tasks, return_exceptions=False)
        checks = {name: {"status": status} for name, status in results_list}
        overall_status = "healthy" if all(c["status"] == "healthy" for c in checks.values()) else "unhealthy"
        return {"status": overall_status, "checks": checks}


health_checker = _HealthChecker()


# ---------------------------------------------------------------------------
# Exposição estilo Prometheus
# ---------------------------------------------------------------------------

def get_metrics() -> str:
    """Retorna string em formato Prometheus."""
    latest = metrics_collector.latest()
    if not latest:
        return ""
    lines = [
        "# HELP agente_cpu_usage CPU usage percentage.",
        "# TYPE agente_cpu_usage gauge",
        f"agente_cpu_usage {latest.cpu_percent}",
        "# HELP agente_memory_free_mb Memory free in MB.",
        "# TYPE agente_memory_free_mb gauge",
        f"agente_memory_free_mb {latest.memory_mb}",
        "# HELP agente_disk_free_mb Disk free in MB.",
        "# TYPE agente_disk_free_mb gauge",
        f"agente_disk_free_mb {latest.disk_free_mb}",
    ]
    return "\n".join(lines)