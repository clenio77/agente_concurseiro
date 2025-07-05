import secrets
from typing import Any, Dict, List, Optional, Union

from pydantic import AnyHttpUrl, BaseSettings, EmailStr, PostgresDsn, validator, ValidationError

class Settings(BaseSettings):
    """
    Configurações da aplicação.
    
    Carrega variáveis de ambiente e define valores padrão.
    """
    # API
    API_PREFIX: str = "/api/v1"
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

    # Validações adicionais
    @validator("DATABASE_URI")
    def validate_database_uri(cls, v):  # noqa: D401
        if not v.startswith(("sqlite:///", "postgresql://")):
            raise ValueError("DATABASE_URI deve começar com sqlite:/// ou postgresql://")
        return v
    SQL_ECHO: bool = False
    CREATE_TABLES_ON_STARTUP: bool = True
    INITIALIZE_DB: bool = True
    
    # Admin inicial
    FIRST_ADMIN_EMAIL: EmailStr = "admin@example.com"
    FIRST_ADMIN_USERNAME: str = "admin"
    FIRST_ADMIN_PASSWORD: str = "admin123"
    
    # Logging
    LOG_LEVEL: str = "INFO"
    
    class Config:
        case_sensitive = True
        env_file = ".env"

# Instância global das configurações
settings = Settings()
