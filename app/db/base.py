from typing import Generator

from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

# Importação condicional para evitar importação circular
try:
    from app.core.config import settings
except ImportError:
    # Fallback para quando executado diretamente
    import os
    DATABASE_URI = os.getenv("DATABASE_URI", "sqlite:///./data/agente_concurseiro.db")
    SQL_ECHO = os.getenv("SQL_ECHO", "false").lower() == "true"

    class Settings:
        DATABASE_URI = DATABASE_URI
        SQL_ECHO = SQL_ECHO

    settings = Settings()

# Criar engine do SQLAlchemy
engine = create_engine(
    settings.DATABASE_URI,
    echo=settings.SQL_ECHO,
)

# Criar sessão
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Base declarativa para modelos
Base = declarative_base()

def get_db() -> Generator:
    """
    Dependency para obter uma sessão do banco de dados.
    
    Yields:
        Sessão do banco de dados
    """
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
