"""
Configuração e gerenciamento do banco de dados
"""

import logging
import os
from contextlib import contextmanager
from typing import Generator

from sqlalchemy import create_engine, event, text
from sqlalchemy.orm import Session, sessionmaker
from sqlalchemy.pool import StaticPool

from .models import Base

# Configuração de logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class DatabaseManager:
    """Gerenciador de banco de dados"""

    def __init__(self):
        self.database_url = self._get_database_url()
        self.engine = self._create_engine()
        self.SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=self.engine)

    def _get_database_url(self) -> str:
        """Obtém URL do banco de dados baseada no ambiente"""

        # Verificar variável de ambiente primeiro
        if database_url := os.getenv("DATABASE_URL"):
            return database_url

        # Configuração baseada no ambiente
        environment = os.getenv("ENVIRONMENT", "development")

        if environment == "production":
            # PostgreSQL para produção
            host = os.getenv("DB_HOST", "localhost")
            port = os.getenv("DB_PORT", "5432")
            database = os.getenv("DB_NAME", "agente_concurseiro")
            username = os.getenv("DB_USER", "postgres")
            password = os.getenv("DB_PASSWORD", "")

            return f"postgresql://{username}:{password}@{host}:{port}/{database}"

        elif environment == "testing":
            # SQLite em memória para testes
            return "sqlite:///:memory:"

        else:
            # SQLite para desenvolvimento
            db_path = os.getenv("DB_PATH", "data/agente_concurseiro.db")
            os.makedirs(os.path.dirname(db_path), exist_ok=True)
            return f"sqlite:///{db_path}"

    def _create_engine(self):
        """Cria engine do SQLAlchemy"""

        if self.database_url.startswith("sqlite"):
            # Configurações específicas para SQLite
            engine = create_engine(
                self.database_url,
                poolclass=StaticPool,
                connect_args={
                    "check_same_thread": False,
                    "timeout": 20
                },
                echo=os.getenv("SQL_DEBUG", "false").lower() == "true"
            )

            # Habilitar foreign keys no SQLite
            @event.listens_for(engine, "connect")
            def set_sqlite_pragma(dbapi_connection, connection_record):
                cursor = dbapi_connection.cursor()
                cursor.execute("PRAGMA foreign_keys=ON")
                cursor.execute("PRAGMA journal_mode=WAL")
                cursor.execute("PRAGMA synchronous=NORMAL")
                cursor.execute("PRAGMA cache_size=1000")
                cursor.execute("PRAGMA temp_store=MEMORY")
                cursor.close()

        else:
            # Configurações para PostgreSQL
            engine = create_engine(
                self.database_url,
                pool_size=int(os.getenv("DB_POOL_SIZE", "10")),
                max_overflow=int(os.getenv("DB_MAX_OVERFLOW", "20")),
                pool_pre_ping=True,
                pool_recycle=3600,
                echo=os.getenv("SQL_DEBUG", "false").lower() == "true"
            )

        return engine

    def create_tables(self):
        """Cria todas as tabelas"""
        try:
            Base.metadata.create_all(bind=self.engine)
            logger.info("✅ Tabelas criadas com sucesso")
        except Exception as e:
            logger.error(f"❌ Erro ao criar tabelas: {e}")
            raise

    def drop_tables(self):
        """Remove todas as tabelas (cuidado!)"""
        try:
            Base.metadata.drop_all(bind=self.engine)
            logger.info("🗑️ Tabelas removidas")
        except Exception as e:
            logger.error(f"❌ Erro ao remover tabelas: {e}")
            raise

    @contextmanager
    def get_session(self) -> Generator[Session, None, None]:
        """Context manager para sessões do banco"""
        session = self.SessionLocal()
        try:
            yield session
            session.commit()
        except Exception as e:
            session.rollback()
            logger.error(f"❌ Erro na sessão do banco: {e}")
            raise
        finally:
            session.close()

    def get_session_sync(self) -> Session:
        """Obtém sessão síncrona (para uso em Streamlit)"""
        return self.SessionLocal()

    def health_check(self) -> bool:
        """Verifica a conexão com o banco de dados."""
        try:
            with self.get_session() as session:
                session.execute(text("SELECT 1"))
            return True
        except Exception as e:
            logger.error(f"❌ Erro na sessão do banco: {e}")
            return False

    def get_stats(self) -> dict:
        """Obtém estatísticas do banco"""
        try:
            with self.get_session() as session:
                from .models import Essay, MockExam, Question, User

                stats = {
                    "users_count": session.query(User).count(),
                    "mock_exams_count": session.query(MockExam).count(),
                    "essays_count": session.query(Essay).count(),
                    "questions_count": session.query(Question).count(),
                    "database_url": self.database_url.split("@")[-1] if "@" in self.database_url else self.database_url,
                    "engine_info": str(self.engine.url)
                }

                return stats
        except Exception as e:
            logger.error(f"❌ Erro ao obter estatísticas: {e}")
            return {"error": str(e)}

# Instância global do gerenciador
db_manager = DatabaseManager()

# Funções de conveniência
def get_db_session():
    """Função para obter sessão do banco (para FastAPI)"""
    session = db_manager.get_session_sync()
    try:
        yield session
    finally:
        session.close()

def init_database():
    """Inicializa o banco de dados"""
    logger.info("🚀 Inicializando banco de dados...")

    # Criar tabelas
    db_manager.create_tables()

    # Verificar saúde
    if db_manager.health_check():
        logger.info("✅ Banco de dados inicializado com sucesso")

        # Exibir estatísticas
        stats = db_manager.get_stats()
        logger.info(f"📊 Estatísticas: {stats}")

        return True
    else:
        logger.error("❌ Falha na inicialização do banco")
        return False

def seed_database():
    """Popula banco com dados iniciais"""
    logger.info("🌱 Populando banco com dados iniciais...")

    try:
        with db_manager.get_session() as session:
            from .models import Question, SystemConfig

            # Configurações do sistema
            configs = [
                {
                    "key": "app_version",
                    "value": {"version": "2.0.0", "build": "production"},
                    "description": "Versão da aplicação",
                    "category": "app"
                },
                {
                    "key": "features",
                    "value": {
                        "gamification": True,
                        "analytics": True,
                        "notifications": True,
                        "essay_evaluation": True
                    },
                    "description": "Funcionalidades habilitadas",
                    "category": "features"
                },
                {
                    "key": "supported_bancas",
                    "value": ["CESPE", "FCC", "VUNESP", "FGV", "IBFC"],
                    "description": "Bancas suportadas pelo sistema",
                    "category": "content"
                }
            ]

            for config_data in configs:
                existing = session.query(SystemConfig).filter_by(key=config_data["key"]).first()
                if not existing:
                    config = SystemConfig(**config_data)
                    session.add(config)

            # Migrar questões do JSON para o banco
            import json
            try:
                with open("data/questions/question_bank.json", "r", encoding="utf-8") as f:
                    question_data = json.load(f)

                questions_added = 0
                for subject, questions in question_data.get("questions", {}).items():
                    for q in questions:
                        existing = session.query(Question).filter_by(external_id=q["id"]).first()
                        if not existing:
                            question = Question(
                                external_id=q["id"],
                                source="internal",
                                text=q["text"],
                                options=q.get("options", []),
                                correct_answer=q["correct_answer"],
                                explanation=q.get("explanation", ""),
                                subject=subject,
                                topic=q.get("topic", ""),
                                difficulty=q.get("difficulty", "medium"),
                                banca=q.get("banca", "CESPE"),
                                year=q.get("year", 2023)
                            )
                            session.add(question)
                            questions_added += 1

                logger.info(f"✅ {questions_added} questões migradas para o banco")

            except FileNotFoundError:
                logger.warning("⚠️ Arquivo de questões não encontrado")

            session.commit()
            logger.info("✅ Dados iniciais inseridos com sucesso")

    except Exception as e:
        logger.error(f"❌ Erro ao popular banco: {e}")
        raise

def backup_database():
    """Cria backup do banco de dados"""
    logger.info("💾 Criando backup do banco...")

    try:
        import shutil
        from datetime import datetime

        if db_manager.database_url.startswith("sqlite"):
            # Backup SQLite
            db_path = db_manager.database_url.replace("sqlite:///", "")
            backup_dir = "backups"
            os.makedirs(backup_dir, exist_ok=True)

            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            backup_path = f"{backup_dir}/backup_{timestamp}.db"

            shutil.copy2(db_path, backup_path)
            logger.info(f"✅ Backup criado: {backup_path}")

            return backup_path
        else:
            # Para PostgreSQL, seria necessário usar pg_dump
            logger.warning("⚠️ Backup automático não implementado para PostgreSQL")
            return None

    except Exception as e:
        logger.error(f"❌ Erro ao criar backup: {e}")
        return None

if __name__ == "__main__":
    # Script para inicializar banco
    print("🚀 Inicializando banco de dados...")

    if init_database():
        print("✅ Banco inicializado com sucesso!")

        # Popular com dados iniciais
        seed_database()
        print("✅ Dados iniciais inseridos!")

        # Criar backup
        backup_path = backup_database()
        if backup_path:
            print(f"✅ Backup criado: {backup_path}")

        print("🎉 Sistema pronto para uso!")
    else:
        print("❌ Falha na inicialização!")
        exit(1)
