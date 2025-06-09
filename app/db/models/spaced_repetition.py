import uuid
from datetime import datetime
from sqlalchemy import Column, String, DateTime, Text, Integer, ForeignKey, JSON, Float, Boolean
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship

from app.db.base import Base

class FlashcardDeck(Base):
    """Modelo de baralho de flashcards no banco de dados."""
    
    __tablename__ = "flashcard_decks"
    
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    user_id = Column(UUID(as_uuid=True), ForeignKey("users.id"), nullable=False)
    title = Column(String(100), nullable=False)
    description = Column(Text)
    subject = Column(String(100), nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # Relacionamentos
    user = relationship("User", back_populates="flashcard_decks")
    flashcards = relationship("Flashcard", back_populates="deck", cascade="all, delete-orphan")
    
    def __repr__(self):
        return f"<FlashcardDeck {self.title}>"

class Flashcard(Base):
    """Modelo de flashcard no banco de dados."""
    
    __tablename__ = "flashcards"
    
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    deck_id = Column(UUID(as_uuid=True), ForeignKey("flashcard_decks.id"), nullable=False)
    front = Column(Text, nullable=False)
    back = Column(Text, nullable=False)
    difficulty = Column(Integer, default=5)  # 1-10
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # Dados de repetição espaçada
    ease_factor = Column(Float, default=2.5)
    interval = Column(Integer, default=1)  # em dias
    last_review = Column(DateTime)
    next_review = Column(DateTime)
    review_count = Column(Integer, default=0)
    
    # Relacionamentos
    deck = relationship("FlashcardDeck", back_populates="flashcards")
    reviews = relationship("FlashcardReview", back_populates="flashcard", cascade="all, delete-orphan")
    
    def __repr__(self):
        return f"<Flashcard {self.id}>"

class FlashcardReview(Base):
    """Modelo de revisão de flashcard no banco de dados."""
    
    __tablename__ = "flashcard_reviews"
    
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    flashcard_id = Column(UUID(as_uuid=True), ForeignKey("flashcards.id"), nullable=False)
    date = Column(DateTime, default=datetime.utcnow, nullable=False)
    quality = Column(Integer, nullable=False)  # 0-5
    time_taken_seconds = Column(Integer)
    ease_factor = Column(Float, nullable=False)
    interval = Column(Integer, nullable=False)  # em dias
    
    # Relacionamentos
    flashcard