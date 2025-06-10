"""
API FastAPI para o Agente Concurseiro
"""

from fastapi import FastAPI, HTTPException, Depends, status, Request
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from fastapi.middleware.cors import CORSMiddleware
from fastapi.middleware.trustedhost import TrustedHostMiddleware
from fastapi.responses import JSONResponse
import uvicorn
import os
from typing import Optional
import logging
from contextlib import asynccontextmanager

from ..db.database import init_database, db_manager
from ..auth.auth_manager import auth_manager, get_current_user
from ..db.models import User
from .routers import auth, users, study_plans, mock_exams, essays, analytics

# Configuração de logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Security
security = HTTPBearer()

@asynccontextmanager
async def lifespan(app: FastAPI):
    """Gerencia ciclo de vida da aplicação"""
    # Startup
    logger.info("🚀 Iniciando Agente Concurseiro API...")
    
    # Inicializar banco de dados
    if not init_database():
        logger.error("❌ Falha na inicialização do banco")
        raise Exception("Database initialization failed")
    
    logger.info("✅ API iniciada com sucesso!")
    
    yield
    
    # Shutdown
    logger.info("🛑 Encerrando API...")

# Criar aplicação FastAPI
app = FastAPI(
    title="Agente Concurseiro API",
    description="API completa para preparação de concursos públicos",
    version="2.0.0",
    docs_url="/docs" if os.getenv("ENVIRONMENT") != "production" else None,
    redoc_url="/redoc" if os.getenv("ENVIRONMENT") != "production" else None,
    lifespan=lifespan
)

# Middleware de CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=os.getenv("ALLOWED_ORIGINS", "*").split(","),
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Middleware de hosts confiáveis (produção)
if os.getenv("ENVIRONMENT") == "production":
    app.add_middleware(
        TrustedHostMiddleware,
        allowed_hosts=os.getenv("ALLOWED_HOSTS", "localhost").split(",")
    )

# Middleware de logging
@app.middleware("http")
async def log_requests(request: Request, call_next):
    """Log de requisições"""
    start_time = time.time()
    
    response = await call_next(request)
    
    process_time = time.time() - start_time
    logger.info(
        f"{request.method} {request.url.path} - "
        f"Status: {response.status_code} - "
        f"Time: {process_time:.3f}s"
    )
    
    return response

# Dependency para obter usuário atual
async def get_current_active_user(credentials: HTTPAuthorizationCredentials = Depends(security)) -> User:
    """Obtém usuário autenticado atual"""
    token = credentials.credentials
    user = get_current_user(token)
    
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Token inválido ou expirado",
            headers={"WWW-Authenticate": "Bearer"},
        )
    
    if not user.is_active:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Usuário inativo"
        )
    
    return user

# Dependency opcional para usuário
async def get_current_user_optional(credentials: Optional[HTTPAuthorizationCredentials] = Depends(security)) -> Optional[User]:
    """Obtém usuário atual (opcional)"""
    if not credentials:
        return None
    
    return get_current_user(credentials.credentials)

# Rotas principais
@app.get("/")
async def root():
    """Endpoint raiz"""
    return {
        "message": "Agente Concurseiro API",
        "version": "2.0.0",
        "status": "online",
        "docs": "/docs"
    }

@app.get("/health")
async def health_check():
    """Health check"""
    db_healthy = db_manager.health_check()
    
    return {
        "status": "healthy" if db_healthy else "unhealthy",
        "database": "connected" if db_healthy else "disconnected",
        "timestamp": datetime.now().isoformat()
    }

@app.get("/stats")
async def get_stats(current_user: User = Depends(get_current_active_user)):
    """Estatísticas do sistema (apenas usuários autenticados)"""
    stats = db_manager.get_stats()
    
    return {
        "system_stats": stats,
        "user_id": current_user.id,
        "timestamp": datetime.now().isoformat()
    }

# Incluir routers
app.include_router(auth.router, prefix="/auth", tags=["Autenticação"])
app.include_router(users.router, prefix="/users", tags=["Usuários"])
app.include_router(study_plans.router, prefix="/study-plans", tags=["Planos de Estudo"])
app.include_router(mock_exams.router, prefix="/mock-exams", tags=["Simulados"])
app.include_router(essays.router, prefix="/essays", tags=["Redações"])
app.include_router(analytics.router, prefix="/analytics", tags=["Analytics"])

# Handler de exceções
@app.exception_handler(HTTPException)
async def http_exception_handler(request: Request, exc: HTTPException):
    """Handler para exceções HTTP"""
    return JSONResponse(
        status_code=exc.status_code,
        content={
            "error": exc.detail,
            "status_code": exc.status_code,
            "timestamp": datetime.now().isoformat()
        }
    )

@app.exception_handler(Exception)
async def general_exception_handler(request: Request, exc: Exception):
    """Handler para exceções gerais"""
    logger.error(f"Erro não tratado: {exc}")
    
    return JSONResponse(
        status_code=500,
        content={
            "error": "Erro interno do servidor",
            "status_code": 500,
            "timestamp": datetime.now().isoformat()
        }
    )

# Configuração para execução
if __name__ == "__main__":
    import time
    from datetime import datetime
    
    # Configurações baseadas no ambiente
    environment = os.getenv("ENVIRONMENT", "development")
    
    if environment == "production":
        # Configurações de produção
        uvicorn.run(
            "app.api.main:app",
            host="0.0.0.0",
            port=int(os.getenv("PORT", 8000)),
            workers=int(os.getenv("WORKERS", 4)),
            log_level="info",
            access_log=True
        )
    else:
        # Configurações de desenvolvimento
        uvicorn.run(
            "app.api.main:app",
            host="127.0.0.1",
            port=8000,
            reload=True,
            log_level="debug"
        )
