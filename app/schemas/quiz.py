from datetime import datetime
from typing import List, Optional
from uuid import UUID

from pydantic import BaseModel, Field

class QuestionBase(BaseModel):
    """
    Schema base para questão de quiz.
    """
    text: str
    options: List[str]
    correct_answer: str
    explanation: Optional[str] = None
    subject: str
    difficulty: str

class QuestionCreate(QuestionBase):
    """
    Schema para criação de questão de quiz.
    """
    pass

class Question(QuestionBase):
    """
    Schema para questão de quiz.
    """
    id: UUID
    quiz_id: UUID
    user_answer: Optional[str] = None
    is_correct: Optional[bool] = None
    time_spent_seconds: Optional[int] = None
    created_at: datetime
    
    class Config:
        orm_mode = True

class QuizBase(BaseModel):
    """
    Schema base para quiz.
    """
    title: str
    description: Optional[str] = None
    difficulty: str
    subjects: List[str]

class QuizCreate(QuizBase):
    """
    Schema para criação de quiz.
    """
    study_plan_id: Optional[UUID] = None
    questions: List[QuestionCreate]

class QuizUpdate(BaseModel):
    """
    Schema para atualização de quiz.
    """
    title: Optional[str] = None
    description: Optional[str] = None
    difficulty: Optional[str] = None
    subjects: Optional[List[str]] = None

class AnswerSubmit(BaseModel):
    """
    Schema para submissão de resposta.
    """
    question_id: UUID
    answer: str
    time_spent_seconds: int

class QuizResult(BaseModel):
    """
    Schema para resultado de quiz.
    """
    answers: List[AnswerSubmit]

class Quiz(QuizBase):
    """
    Schema para quiz.
    """
    id: UUID
    user_id: UUID
    study_plan_id: Optional[UUID] = None
    is_completed: bool
    score: Optional[float] = None
    started_at: Optional[datetime] = None
    completed_at: Optional[datetime] = None
    created_at: datetime
    updated_at: datetime
    questions: List[Question]
    
    class Config:
        orm_mode = True
