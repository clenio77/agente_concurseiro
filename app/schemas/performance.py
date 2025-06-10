from datetime import date, datetime
from typing import Dict, List, Optional
from uuid import UUID

from pydantic import BaseModel

# Schemas para registro de desempenho
class PerformanceRecordBase(BaseModel):
    """
    Schema base para registro de desempenho.
    """
    date: date
    study_time_minutes: int
    subjects_studied: List[Dict]  # Lista de matérias estudadas com tempo
    quiz_scores: Optional[List[Dict]] = None  # Lista de pontuações em quizzes
    flashcard_stats: Optional[Dict] = None  # Estatísticas de flashcards
    notes: Optional[str] = None

class PerformanceRecordCreate(PerformanceRecordBase):
    """
    Schema para criação de registro de desempenho.
    """
    study_plan_id: Optional[UUID] = None

class PerformanceRecordUpdate(BaseModel):
    """
    Schema para atualização de registro de desempenho.
    """
    date: Optional[date] = None
    study_time_minutes: Optional[int] = None
    subjects_studied: Optional[List[Dict]] = None
    quiz_scores: Optional[List[Dict]] = None
    flashcard_stats: Optional[Dict] = None
    notes: Optional[str] = None

class PerformanceRecord(PerformanceRecordBase):
    """
    Schema para registro de desempenho.
    """
    id: UUID
    user_id: UUID
    study_plan_id: Optional[UUID] = None
    created_at: datetime
    updated_at: datetime
    
    class Config:
        orm_mode = True

# Schema para estatísticas de desempenho
class PerformanceStats(BaseModel):
    """
    Schema para estatísticas de desempenho.
    """
    total_study_time: int
    subject_distribution: Dict[str, int]
    quiz_average_score: float
    flashcard_retention_rate: float
    study_streak: int
    weekly_progress: List[Dict]
    monthly_progress: List[Dict]
