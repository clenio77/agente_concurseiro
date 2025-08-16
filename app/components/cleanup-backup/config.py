from __future__ import annotations

import secrets
from typing import List, Optional, Union

from pydantic import AnyHttpUrl, EmailStr, validator
from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    """
    Configurações da aplicação.
    
    Carrega variáveis de ambiente e define valores padrão.
    """
    # API
    API_PREFIX: str = "/api/v1"
    API_BASE_URL: str = "http://localhost:8000"  # URL base para o backend FastAPI
    PROJECT_NAME: str = "Assistente de Preparação para Concursos"
    PROJECT_DESCRIPTION: str = "API para o Assistente de Preparação para Concursos Públicos"
    PROJECT_VERSION: str = "0.1.0"

    # Segurança
    SECRET_KEY: str = secrets.token_urlsafe(32)
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 60 * 24 * 7  # 7 dias

    # CORS
    BACKEND_CORS_ORIGINS: List[AnyHttpUrl] = []

    @validator("BACKEND_CORS_ORIGINS", pre=True)
    def assemble_cors_origins(cls, v: Union[str, List[str]]) -> Union[List[str], str]:
        if isinstance(v, str) and not v.startswith("["):
            return [i.strip() for i in v.split(",")]
        elif isinstance(v, (list, str)):
            return v
        raise ValueError(v)

    # Banco de Dados
    DATABASE_URI: str = "sqlite:///./app.db"
    SQL_ECHO: bool = False
    CREATE_TABLES_ON_STARTUP: bool = True
    INITIALIZE_DB: bool = True

    # Admin inicial
    FIRST_ADMIN_EMAIL: EmailStr = "admin@example.com"
    FIRST_ADMIN_USERNAME: str = "admin"
    FIRST_ADMIN_PASSWORD: str = "admin123"

    # Logging
    LOG_LEVEL: str = "INFO"

    # Environment
    ENVIRONMENT: str = "development"

    # Database
    DATABASE_URL: str = "sqlite:///./data/agente_concurseiro.db"

    # JWT
    ALGORITHM: str = "HS256"

    # CORS
    ALLOWED_ORIGINS: List[str] = ["http://localhost:3000", "http://localhost:8501"]

    # Email
    SMTP_SERVER: Optional[str] = None
    SMTP_PORT: int = 587
    SMTP_USER: Optional[str] = None
    SMTP_PASSWORD: Optional[str] = None

    # AWS
    AWS_ACCESS_KEY_ID: Optional[str] = None
    AWS_SECRET_ACCESS_KEY: Optional[str] = None
    AWS_REGION: str = "us-east-1"
    AWS_S3_BUCKET: Optional[str] = None

    # Redis
    REDIS_URL: Optional[str] = None

    # Firebase
    FIREBASE_SERVER_KEY: Optional[str] = None

    # Frontend
    FRONTEND_URL: str = "http://localhost:8501"

    class Config:
        case_sensitive = True
        env_file = ".env"

# Instância global das configurações
settings = Settings()
