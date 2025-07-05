"""Rotas de health check."""
from __future__ import annotations

import time
from fastapi import APIRouter, status

router = APIRouter()


@router.get("/health", status_code=status.HTTP_200_OK)
async def health_check():  # noqa: D401
    """Endpoint simples que retorna status=ok e timestamp."""
    return {"status": "ok", "timestamp": int(time.time())}