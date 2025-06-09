from datetime import datetime
from typing import List, Optional
from uuid import UUID

from pydantic import BaseModel

class FlashcardBase(BaseModel):
    """
    Schema base para flashcard.
    """
    front: str
    back: str
    subject: str
    difficulty: str

class FlashcardCreate(FlashcardBase):
    """
    Schema para criação de flashcard.
    """
    pass

class FlashcardUpdate(BaseModel):
    """
    Schema para atualização de flashcard.
    """
    front: Optional[str] = None
    back: Optional[str] = None
    subject: Optional[str] = None
    difficulty: Optional[str] = None

class FlashcardReviewCreate(BaseModel):
    """
    Schema para criação de revisão de flashcard.
    """
    quality: int  # 0-5, onde 0 é "não lembrei" e 5 é "lembrei perfeitamente"

class FlashcardReview(FlashcardReviewCreate):
    """
    Schema para revisão de flashcard.
    """
    id: UUID
    flashcard_id: UUID
    created_at: datetime
    
    class Config:
        orm_mode = True

class Flashcard(FlashcardBase):
    """
    Schema para flashcard.
    """
    id: UUID
    user_id: UUID
    interval: float
    ease_factor: float
    next_review: datetime
    created_at: datetime
    updated_at: datetime
    reviews: List[FlashcardReview]
    
    class Config:
        orm_mode = True
