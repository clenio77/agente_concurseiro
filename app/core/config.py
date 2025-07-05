"""Configuração central da aplicação usando pydantic-settings v2."""

from __future__ import annotations

import secrets
from typing import List

from pydantic import AnyHttpUrl, EmailStr, Field, PostgresDsn, ValidationError
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    """Carrega variáveis de ambiente de maneira segura."""

    model_config = SettingsConfigDict(env_file=".env", case_sensitive=True)

    # Ambiente
    ENVIRONMENT: str = Field("development", pattern="^(development|staging|production)$")

    # API
    API_PREFIX: str = "/api/v1"
    PROJECT_NAME: str = "Assistente de Preparação para Concursos"
    PROJECT_DESCRIPTION: str = "API para o Assistente de Preparação para Concursos Públicos"
    PROJECT_VERSION: str = "0.1.0"

    # Segurança
    JWT_SECRET: str = Field(..., min_length=32)
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 60 * 24 * 7

    # CORS
    BACKEND_CORS_ORIGINS: List[AnyHttpUrl] = []

    # Banco de Dados (PostgreSQL recomendado em produção)
    DB_HOST: str = "localhost"
    DB_PORT: int = 5432
    DB_USER: str = "postgres"
    DB_PASSWORD: str = "postgres"
    DB_NAME: str = "agente_concurseiro"

    SQL_ECHO: bool = False

    @property
    def DATABASE_URI(self) -> str:  # noqa: D401
        return f"postgresql://{self.DB_USER}:{self.DB_PASSWORD}@{self.DB_HOST}:{self.DB_PORT}/{self.DB_NAME}"


# Instância global
try:
    settings = Settings()  # noqa: S703
except ValidationError as exc:  # pragma: no cover
    # Exibir erro amigável no startup
    import sys, json  # noqa: WPS433

    sys.stderr.write("\n[CONFIG] Variáveis de ambiente inválidas:\n")
    sys.stderr.write(exc.json())
    sys.exit(1)
