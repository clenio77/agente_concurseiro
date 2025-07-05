"""Ponto de entrada principal da aplicação FastAPI.

Esta versão inclui:
• Logging estruturado configurado via `app.core.logging_config`.
• Middlewares: cabeçalhos de segurança, rate-limiting e tratamento de erros.
• Rota `/health` para liveness/readiness checks.
"""

from __future__ import annotations

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.api.api import api_router
from app.core.config import settings
from app.core.lifespan import lifespan
from app.core.logging_config import configure_logging
from app.middleware.security_headers import add_security_headers
from app.middleware.error_handler import add_error_handler
from app.middleware.rate_limit import add_rate_limit
from app.api.routes.health import router as health_router

configure_logging()

# Criar aplicação FastAPI
app = FastAPI(
    title=settings.PROJECT_NAME,
    description=settings.PROJECT_DESCRIPTION,
    version=settings.PROJECT_VERSION,
    openapi_url=f"{settings.API_PREFIX}/openapi.json",
    docs_url=f"{settings.API_PREFIX}/docs",
    redoc_url=f"{settings.API_PREFIX}/redoc",
    lifespan=lifespan,
)

# Configurar CORS para permitir requisições de origens definidas
if settings.BACKEND_CORS_ORIGINS:
    app.add_middleware(
        CORSMiddleware,
        allow_origins=[str(origin) for origin in settings.BACKEND_CORS_ORIGINS],
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )

# Incluir rotas da API principal
app.include_router(api_router, prefix=settings.API_PREFIX)

# Rota de health check (não necessita autenticação)
app.include_router(health_router, prefix="")

# Middlewares adicionais
add_security_headers(app)
add_error_handler(app)
add_rate_limit(app)

# Rota raiz para verificação rápida da API
@app.get("/")
async def root():
    """
    Endpoint raiz da API.
    Retorna mensagem de boas-vindas e link para a documentação.
    """
    return {
        "message": "Bem-vindo à API do Assistente de Preparação para Concursos",
        "docs": f"{settings.API_PREFIX}/docs",
    }
