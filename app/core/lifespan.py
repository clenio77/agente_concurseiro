from contextlib import asynccontextmanager
from typing import AsyncGenerator

from fastapi import FastAPI
from sqlalchemy.orm import Session

from app.db.base import engine, Base
from app.db.init_db import init_db
from app.core.config import settings
from app.core.logger import logger

@asynccontextmanager
async def lifespan(app: FastAPI) -> AsyncGenerator[None, None]:
    """
    Gerencia o ciclo de vida da aplicação.
    
    Este contexto assíncrono é executado na inicialização e encerramento da aplicação.
    """
    # Inicialização
    logger.info("Iniciando aplicação...")
    
    # Criar tabelas no banco de dados
    if settings.CREATE_TABLES_ON_STARTUP:
        logger.info("Criando tabelas no banco de dados...")
        Base.metadata.create_all(bind=engine)
    
    # Inicializar dados iniciais
    if settings.INITIALIZE_DB:
        logger.info("Inicializando dados no banco de dados...")
        init_db()
    
    # Inicializar outros recursos
    logger.info("Aplicação iniciada com sucesso!")
    
    yield  # Aqui a aplicação está em execução
    
    # Limpeza ao encerrar
    logger.info("Encerrando aplicação...")
    
    # Liberar recursos
    logger.info("Aplicação encerrada com sucesso!")