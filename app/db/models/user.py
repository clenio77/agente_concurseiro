"""
Modelo ORM do usuário.
Define a estrutura da tabela de usuários e seus relacionamentos no banco de dados.
"""

import uuid
from datetime import datetime

from sqlalchemy import Boolean, Column, DateTime, String
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship

from app.db.base import Base

class User(Base):
    """
    Modelo de usuário no banco de dados.
    Representa um usuário do sistema, incluindo autenticação, permissões e relacionamentos.
    """
    __tablename__ = "users"
    
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    email = Column(String, unique=True, index=True, nullable=False)
    username = Column(String, unique=True, index=True, nullable=False)
    hashed_password = Column(String, nullable=False)
    full_name = Column(String, nullable=True)
    is_active = Column(Boolean, default=True)
    is_admin = Column(Boolean, default=False)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # Relacionamentos com outras tabelas
    study_plans = relationship("StudyPlan", back_populates="user", cascade="all, delete-orphan")
    quizzes = relationship("Quiz", back_populates="user", cascade="all, delete-orphan")
    flashcards = relationship("Flashcard", back_populates="user", cascade="all, delete-orphan")
    performance_records = relationship("PerformanceRecord", back_populates="user", cascade="all, delete-orphan")
    
    def __repr__(self):
        """
        Retorna uma representação legível do usuário.
        """
        return f"<User {self.username}>"
