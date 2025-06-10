from datetime import datetime
from typing import Dict, List, Optional
from uuid import UUID

from pydantic import BaseModel

class StudyPlanBase(BaseModel):
    """
    Schema base para plano de estudos.
    """
    title: str
    description: Optional[str] = None
    cargo: str
    concurso: str
    banca: str
    cidade: str
    study_hours_per_week: int
    duration_months: int
    content: Dict  # Conteúdo do plano de estudos em formato JSON

class StudyPlanCreate(StudyPlanBase):
    """
    Schema para criação de plano de estudos.
    """
    start_date: Optional[datetime] = None
    is_active: bool = True

class StudyPlanUpdate(BaseModel):
    """
    Schema para atualização de plano de estudos.
    """
    title: Optional[str] = None
    description: Optional[str] = None
    cargo: Optional[str] = None
    concurso: Optional[str] = None
    banca: Optional[str] = None
    cidade: Optional[str] = None
    study_hours_per_week: Optional[int] = None
    duration_months: Optional[int] = None
    content: Optional[Dict] = None
    is_active: Optional[bool] = None

class StudyPlan(StudyPlanBase):
    """
    Schema para plano de estudos.
    """
    id: UUID
    user_id: UUID
    start_date: datetime
    end_date: datetime
    is_active: bool
    created_at: datetime
    updated_at: datetime
    
    class Config:
        orm_mode = True
