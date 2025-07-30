"""
Configuração otimizada para deploy no Vercel
"""

import os
import tempfile
from typing import Optional
from sqlalchemy import create_engine, text
from sqlalchemy.orm import sessionmaker
from sqlalchemy.pool import StaticPool
import streamlit as st

class VercelConfig:
    """Configurações específicas para Vercel"""
    
    def __init__(self):
        self.is_vercel = self._is_vercel_environment()
        self.database_url = self._get_database_url()
        self.temp_dir = self._get_temp_directory()
    
    def _is_vercel_environment(self) -> bool:
        """Detecta se está rodando no Vercel"""
        return (
            os.getenv("VERCEL") == "1" or 
            os.getenv("VERCEL_ENV") is not None or
            os.getenv("NOW_REGION") is not None
        )
    
    def _get_database_url(self) -> str:
        """Obtém URL do banco baseada no ambiente"""
        
        # Prioridade 1: Variável de ambiente explícita
        if database_url := os.getenv("DATABASE_URL"):
            return database_url
        
        # Prioridade 2: Configuração Supabase
        if self._has_supabase_config():
            return self._build_supabase_url()
        
        # Prioridade 3: Configuração PostgreSQL genérica
        if self._has_postgres_config():
            return self._build_postgres_url()
        
        # Fallback: SQLite local (apenas desenvolvimento)
        if not self.is_vercel:
            return "sqlite:///data/agente_concurseiro.db"
        
        # Erro: Vercel sem banco configurado
        raise ValueError(
            "❌ Banco de dados não configurado para Vercel! "
            "Configure DATABASE_URL ou variáveis do Supabase."
        )
    
    def _has_supabase_config(self) -> bool:
        """Verifica se tem configuração do Supabase"""
        return all([
            os.getenv("SUPABASE_URL"),
            os.getenv("SUPABASE_KEY"),
            os.getenv("SUPABASE_DB_PASSWORD")
        ])
    
    def _build_supabase_url(self) -> str:
        """Constrói URL do Supabase"""
        url = os.getenv("SUPABASE_URL")
        password = os.getenv("SUPABASE_DB_PASSWORD")
        
        # Extrair host do URL do Supabase
        host = url.replace("https://", "").replace("http://", "")
        
        return f"postgresql://postgres:{password}@db.{host}:5432/postgres"
    
    def _has_postgres_config(self) -> bool:
        """Verifica se tem configuração PostgreSQL genérica"""
        return all([
            os.getenv("POSTGRES_HOST"),
            os.getenv("POSTGRES_USER"),
            os.getenv("POSTGRES_PASSWORD"),
            os.getenv("POSTGRES_DB")
        ])
    
    def _build_postgres_url(self) -> str:
        """Constrói URL PostgreSQL genérica"""
        host = os.getenv("POSTGRES_HOST")
        port = os.getenv("POSTGRES_PORT", "5432")
        user = os.getenv("POSTGRES_USER")
        password = os.getenv("POSTGRES_PASSWORD")
        database = os.getenv("POSTGRES_DB")
        
        return f"postgresql://{user}:{password}@{host}:{port}/{database}"
    
    def _get_temp_directory(self) -> str:
        """Obtém diretório temporário apropriado"""
        if self.is_vercel:
            return "/tmp"
        else:
            return tempfile.gettempdir()
    
    def get_database_engine(self):
        """Cria engine do banco de dados"""
        
        if self.database_url.startswith("sqlite"):
            # Configuração SQLite (desenvolvimento)
            engine = create_engine(
                self.database_url,
                poolclass=StaticPool,
                connect_args={"check_same_thread": False},
                echo=False
            )
        else:
            # Configuração PostgreSQL (produção)
            engine = create_engine(
                self.database_url,
                pool_size=5,
                max_overflow=10,
                pool_pre_ping=True,
                pool_recycle=300,  # 5 minutos (menor para Vercel)
                echo=False
            )
        
        return engine
    
    def save_uploaded_file(self, uploaded_file) -> str:
        """Salva arquivo temporariamente"""
        file_extension = uploaded_file.name.split('.')[-1]
        temp_path = os.path.join(
            self.temp_dir, 
            f"uploaded_{hash(uploaded_file.name)}.{file_extension}"
        )
        
        with open(temp_path, "wb") as f:
            f.write(uploaded_file.getvalue())
        
        return temp_path
    
    def cleanup_temp_file(self, file_path: str):
        """Remove arquivo temporário"""
        try:
            if os.path.exists(file_path):
                os.remove(file_path)
        except Exception as e:
            st.warning(f"⚠️ Não foi possível remover arquivo temporário: {e}")
    
    def get_environment_info(self) -> dict:
        """Retorna informações do ambiente"""
        return {
            "is_vercel": self.is_vercel,
            "database_type": "PostgreSQL" if not self.database_url.startswith("sqlite") else "SQLite",
            "temp_dir": self.temp_dir,
            "vercel_region": os.getenv("VERCEL_REGION", "N/A"),
            "vercel_env": os.getenv("VERCEL_ENV", "N/A")
        }

# Instância global
vercel_config = VercelConfig()

# Funções de conveniência
def is_vercel() -> bool:
    """Verifica se está no Vercel"""
    return vercel_config.is_vercel

def get_database_engine():
    """Obtém engine do banco"""
    return vercel_config.get_database_engine()

def save_temp_file(uploaded_file) -> str:
    """Salva arquivo temporário"""
    return vercel_config.save_uploaded_file(uploaded_file)

def cleanup_temp_file(file_path: str):
    """Remove arquivo temporário"""
    vercel_config.cleanup_temp_file(file_path)
