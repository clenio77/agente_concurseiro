from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.api.api import api_router
from app.core.config import settings
from app.core.lifespan import lifespan

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

# Configurar CORS
if settings.BACKEND_CORS_ORIGINS:
    app.add_middleware(
        CORSMiddleware,
        allow_origins=[str(origin) for origin in settings.BACKEND_CORS_ORIGINS],
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )

# Incluir rotas da API
app.include_router(api_router, prefix=settings.API_PREFIX)

# Rota raiz
@app.get("/")
async def root():
    return {
        "message": "Bem-vindo à API do Assistente de Preparação para Concursos",
        "docs": f"{settings.API_PREFIX}/docs",
    }
