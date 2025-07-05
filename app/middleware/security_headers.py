"""Middleware para injetar cabeçalhos de segurança em todas as respostas."""
from __future__ import annotations

from typing import Callable, Awaitable

from fastapi import FastAPI
from fastapi.responses import Response

# Lista de cabeçalhos padrão (pode ser estendida via settings futuramente)
_DEFAULT_HEADERS = {
    "X-Content-Type-Options": "nosniff",
    "X-Frame-Options": "DENY",
    "X-XSS-Protection": "1; mode=block",
    "Referrer-Policy": "same-origin",
    "Strict-Transport-Security": "max-age=63072000; includeSubDomains; preload",
    "Cache-Control": "no-store",
}


def add_security_headers(app: FastAPI) -> None:  # noqa: D401
    """Registra evento de resposta para anexar cabeçalhos."""

    @app.middleware("http")  # type: ignore[attr-defined]
    async def _security_headers_middleware(request, call_next: Callable[..., Awaitable[Response]]):  # noqa: D401
        response: Response = await call_next(request)
        for key, value in _DEFAULT_HEADERS.items():
            response.headers.setdefault(key, value)
        return response