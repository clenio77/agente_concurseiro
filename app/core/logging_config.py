"""Configuração de logging estruturado.
Tenta utilizar **structlog**; se indisponível, cai para logging padrão.
"""
from __future__ import annotations

import logging
import sys
from typing import Any

try:
    import structlog  # type: ignore

    def configure_logging(level: int | str = logging.INFO) -> None:  # noqa: D401
        """Configura structlog com saída JSON simplificada."""
        shared_processors: list[Any] = [
            structlog.processors.TimeStamper(fmt="iso"),
            structlog.processors.add_log_level,
        ]
        structlog.configure(
            processors=[
                *shared_processors,
                structlog.processors.JSONRenderer(),
            ],
            wrapper_class=structlog.make_filtering_bound_logger(level),
            logger_factory=structlog.PrintLoggerFactory(file=sys.stdout),
        )

except ModuleNotFoundError:  # pragma: no cover
    # Fallback para logging padrão
    def configure_logging(level: int | str = logging.INFO) -> None:  # type: ignore[override] # noqa: D401
        logging.basicConfig(
            level=level,
            format="%(asctime)s [%(levelname)s] %(name)s: %(message)s",
            stream=sys.stdout,
        )