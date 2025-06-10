import logging
from sqlalchemy.orm import Session

from app.core.config import settings
from app.core.security import get_password_hash
from app.db.base import SessionLocal
from app.db.models.user import User

logger = logging.getLogger(__name__)

def init_db() -> None:
    """
    Inicializa o banco de dados com dados iniciais.
    """
    db = SessionLocal()
    try:
        # Criar usuário admin se não existir
        create_admin_user(db)
    finally:
        db.close()

def create_admin_user(db: Session) -> None:
    """
    Cria o usuário administrador inicial se não existir.
    
    Args:
        db: Sessão do banco de dados
    """
    # Verificar se já existe um usuário admin
    admin = db.query(User).filter(User.email == settings.FIRST_ADMIN_EMAIL).first()
    if admin:
        logger.info("Usuário admin já existe")
        return
    
    # Criar usuário admin
    admin_user = User(
        email=settings.FIRST_ADMIN_EMAIL,
        username=settings.FIRST_ADMIN_USERNAME,
        hashed_password=get_password_hash(settings.FIRST_ADMIN_PASSWORD),
        full_name="Administrador",
        is_active=True,
        is_admin=True,
    )
    
    db.add(admin_user)
    db.commit()
    logger.info("Usuário admin criado com sucesso")