"""Middleware simples para capturar exceções e retornar resposta JSON padronizada."""
from __future__ import annotations

import logging
from typing import Callable, Awaitable

from fastapi import FastAPI, HTTPException
from fastapi.responses import JSONResponse

_logger = logging.getLogger(__name__)


def add_error_handler(app: FastAPI) -> None:  # noqa: D401
    """Registra middleware de tratamento de erros."""

    @app.middleware("http")  # type: ignore[attr-defined]
    async def _error_middleware(request, call_next: Callable[..., Awaitable[JSONResponse]]):  # noqa: D401
        try:
            return await call_next(request)
        except HTTPException as exc:
            _logger.warning("Handled HTTPException: %s", exc.detail)
            return JSONResponse(status_code=exc.status_code, content={"detail": exc.detail})
        except Exception as exc:  # noqa: BLE001
            _logger.exception("Unhandled exception: %s", exc)
            return JSONResponse(status_code=500, content={"detail": "Internal Server Error"})