import uuid
from datetime import datetime
from typing import List

from sqlalchemy import Boolean, Column, DateTime, ForeignKey, Float, Integer, String, Text, JSON
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship

from app.db.base import Base

class PerformanceRecord(Base):
    """
    Modelo de registro de desempenho no banco de dados.
    """
    __tablename__ = "performance_records"
    
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    user_id = Column(UUID(as_uuid=True), ForeignKey("users.id"), nullable=False)
    study_plan_id = Column(UUID(as_uuid=True), ForeignKey("study_plans.id"), nullable=True)
    date = Column(DateTime, nullable=False, default=datetime.utcnow)
    study_time_minutes = Column(Integer, nullable=False)
    subjects_studied = Column(JSON, nullable=False)  # Lista de matérias estudadas em formato JSON
    quiz_scores = Column(JSON, nullable=True)  # Pontuações de quizzes em formato JSON
    flashcard_stats = Column(JSON, nullable=True)  # Estatísticas de flashcards em formato JSON
    notes = Column(Text, nullable=True)
    created_at = Column(DateTime, default=datetime.utcnow)
    
    # Relacionamentos
    user = relationship("User", back_populates="performance_records")
    study_plan = relationship("StudyPlan", back_populates="performance_records")
    
    def __repr__(self):
        return f"<PerformanceRecord {self.date} - {self.study_time_minutes} minutes>"
