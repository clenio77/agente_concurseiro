import uuid
from datetime import datetime
from typing import List

from sqlalchemy import Boolean, Column, DateTime, ForeignKey, Float, Integer, String, Text, JSON
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship

from app.db.base import Base

class Quiz(Base):
    """
    Modelo de quiz no banco de dados.
    """
    __tablename__ = "quizzes"
    
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    user_id = Column(UUID(as_uuid=True), ForeignKey("users.id"), nullable=False)
    study_plan_id = Column(UUID(as_uuid=True), ForeignKey("study_plans.id"), nullable=True)
    title = Column(String, nullable=False)
    description = Column(Text, nullable=True)
    difficulty = Column(String, nullable=False)
    subjects = Column(JSON, nullable=False)  # Lista de matérias em formato JSON
    is_completed = Column(Boolean, default=False)
    score = Column(Float, nullable=True)
    started_at = Column(DateTime, nullable=True)
    completed_at = Column(DateTime, nullable=True)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # Relacionamentos
    user = relationship("User", back_populates="quizzes")
    study_plan = relationship("StudyPlan", back_populates="quizzes")
    questions = relationship("QuizQuestion", back_populates="quiz", cascade="all, delete-orphan")

class QuizQuestion(Base):
    """
    Modelo de questão de quiz no banco de dados.
    """
    __tablename__ = "quiz_questions"
    
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    quiz_id = Column(UUID(as_uuid=True), ForeignKey("quizzes.id"), nullable=False)
    text = Column(Text, nullable=False)
    options = Column(JSON, nullable=False)  # Lista de opções em formato JSON
    correct_answer = Column(String, nullable=False)
    explanation = Column(Text, nullable=True)
    subject = Column(String, nullable=False)
    difficulty = Column(String, nullable=False)
    user_answer = Column(String, nullable=True)
    is_correct = Column(Boolean, nullable=True)
    time_spent_seconds = Column(Integer, nullable=True)
    created_at = Column(DateTime, default=datetime.utcnow)
    
    # Relacionamentos
    quiz = relationship("Quiz", back_populates="questions")
