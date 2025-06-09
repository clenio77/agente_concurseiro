from typing import Generator

from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

from app.core.config import settings

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
