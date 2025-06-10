import uuid
from datetime import datetime
from typing import List

from sqlalchemy import Boolean, Column, DateTime, ForeignKey, Integer, String, Text
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship

from app.db.base import Base

class Flashcard(Base):
    """
    Modelo de flashcard no banco de dados.
    """
    __tablename__ = "flashcards"
    
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    user_id = Column(UUID(as_uuid=True), ForeignKey("users.id"), nullable=False)
    front = Column(Text, nullable=False)
    back = Column(Text, nullable=False)
    subject = Column(String, nullable=False)
    difficulty = Column(Integer, nullable=False, default=3)  # 1-5
    next_review = Column(DateTime, nullable=False, default=datetime.utcnow)
    interval = Column(Integer, nullable=False, default=1)  # Em dias
    ease_factor = Column(Float, nullable=False, default=2.5)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # Relacionamentos
    user = relationship("User", back_populates="flashcards")
    reviews = relationship("FlashcardReview", back_populates="flashcard", cascade="all, delete-orphan")

class FlashcardReview(Base):
    """
    Modelo de revisão de flashcard no banco de dados.
    """
    __tablename__ = "flashcard_reviews"
    
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    flashcard_id = Column(UUID(as_uuid=True), ForeignKey("flashcards.id"), nullable=False)
    quality = Column(Integer, nullable=False)  # 0-5
    review_date = Column(DateTime, default=datetime.utcnow)
    
    # Relacionamentos
    flashcard = relationship("Flashcard", back_populates="reviews")