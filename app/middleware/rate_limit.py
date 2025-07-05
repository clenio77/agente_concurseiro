"""Middleware simples de rate-limiting por IP (token bucket em memória)."""
from __future__ import annotations

import asyncio
import time
from typing import Callable, Awaitable, Dict

from fastapi import FastAPI, HTTPException, status

# Configurações padrão – 100 requisições por 60s
_MAX_REQUESTS = 100
_WINDOW = 60


class _Bucket:
    __slots__ = ("tokens", "last_refill")

    def __init__(self):
        self.tokens = _MAX_REQUESTS
        self.last_refill = time.time()

    def consume(self) -> bool:  # noqa: D401
        now = time.time()
        elapsed = now - self.last_refill
        # Recarrega tokens proporcionalmente
        refill = int(elapsed / _WINDOW * _MAX_REQUESTS)
        if refill:
            self.tokens = min(_MAX_REQUESTS, self.tokens + refill)
            self.last_refill = now
        if self.tokens:
            self.tokens -= 1
            return True
        return False


_buckets: Dict[str, _Bucket] = {}
_lock = asyncio.Lock()


async def _get_bucket(ip: str) -> _Bucket:  # noqa: D401
    async with _lock:
        bucket = _buckets.get(ip)
        if bucket is None:
            bucket = _Bucket()
            _buckets[ip] = bucket
        return bucket


def add_rate_limit(app: FastAPI) -> None:  # noqa: D401
    """Adiciona middleware de rate-limiting ao aplicativo."""

    @app.middleware("http")  # type: ignore[attr-defined]
    async def _rate_limit_middleware(request, call_next: Callable[..., Awaitable]):  # noqa: D401
        client_ip = request.client.host if request.client else "unknown"
        bucket = await _get_bucket(client_ip)
        if not bucket.consume():
            raise HTTPException(status_code=status.HTTP_429_TOO_MANY_REQUESTS, detail="Rate limit exceeded")
        return await call_next(request)