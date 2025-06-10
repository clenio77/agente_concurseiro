import uuid
from datetime import datetime

from sqlalchemy import Boolean, Column, DateTime, ForeignKey, Integer, JSON, String, Text
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship

from app.db.base import Base

class StudyPlan(Base):
    """
    Modelo de plano de estudos no banco de dados.
    """
    __tablename__ = "study_plans"
    
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    user_id = Column(UUID(as_uuid=True), ForeignKey("users.id"), nullable=False)
    title = Column(String, nullable=False)
    description = Column(Text, nullable=True)
    cargo = Column(String, nullable=False)
    concurso = Column(String, nullable=False)
    banca = Column(String, nullable=False)
    cidade = Column(String, nullable=False)
    study_hours_per_week = Column(Integer, nullable=False)
    duration_months = Column(Integer, nullable=False)
    start_date = Column(DateTime, nullable=False)
    end_date = Column(DateTime, nullable=False)
    content = Column(JSON, nullable=False)  # Conteúdo do plano de estudos em formato JSON
    is_active = Column(Boolean, default=True)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # Relacionamentos
    user = relationship("User", back_populates="study_plans")
    quizzes = relationship("Quiz", back_populates="study_plan", cascade="all, delete-orphan")
    performance_records = relationship("PerformanceRecord", back_populates="study_plan", cascade="all, delete-orphan")



