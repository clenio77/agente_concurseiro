from typing import Any, List

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.api.deps import get_current_user
from app.db.base import get_db
from app.db.models.performance import PerformanceRecord
from app.db.models.study_plan import StudyPlan
from app.db.models.user import User
from app.schemas.performance import (
    PerformanceRecord as PerformanceRecordSchema,
    PerformanceRecordCreate,
    PerformanceRecordUpdate,
    PerformanceStats,
)

router = APIRouter()

@router.get("/", response_model=List[PerformanceRecordSchema])
def read_performance_records(
    db: Session = Depends(get_db),
    skip: int = 0,
    limit: int = 100,
    current_user: User = Depends(get_current_user),
) -> Any:
    """
    Recupera todos os registros de desempenho do usuário atual.
    """
    records = (
        db.query(PerformanceRecord)
        .filter(PerformanceRecord.user_id == current_user.id)
        .offset(skip)
        .limit(limit)
        .all()
    )
    return records

@router.post("/", response_model=PerformanceRecordSchema)
def create_performance_record(
    *,
    db: Session = Depends(get_db),
    record_in: PerformanceRecordCreate,
    current_user: User = Depends(get_current_user),
) -> Any:
    """
    Cria um novo registro de desempenho.
    """
    # Verificar se o plano de estudos existe
    if record_in.study_plan_id:
        study_plan = db.query(StudyPlan).filter(
            StudyPlan.id == record_in.study_plan_id,
            StudyPlan.user_id == current_user.id
        ).first()
        if not study_plan:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Plano de estudos não encontrado",
            )
    
    # Criar registro de desempenho
    record = PerformanceRecord(
        user_id=current_user.id,
        study_plan_id=record_in.study_plan_id,
        date=record_in.date,
        study_time_minutes=record_in.study_time_minutes,
        subjects_studied=record_in.subjects_studied,
        quiz_scores=record_in.quiz_scores,
        flashcard_stats=record_in.flashcard_stats,
        notes=record_in.notes,
    )
    db.add(record)
    db.commit()
    db.refresh(record)
    return record

@router.get("/stats", response_model=PerformanceStats)
def get_performance_stats(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
) -> Any:
    """
    Recupera estatísticas de desempenho do usuário atual.
    """
    # Implementar lógica para calcular estatísticas de desempenho
    # Este é um exemplo simplificado
    
    # Total de tempo de estudo
    records = db.query(PerformanceRecord).filter(
        PerformanceRecord.user_id == current_user.id
    ).all()
    
    total_study_time = sum(record.study_time_minutes for record in records)
    
    # Distribuição por matéria
    subject_distribution = {}
    for record in records:
        for subject in record.subjects_studied:
            subject_name = subject.get("name", "Desconhecido")
            subject_time = subject.get("time_minutes", 0)
            if subject_name in subject_distribution:
                subject_distribution[subject_name] += subject_time
            else:
                subject_distribution[subject_name] = subject_time
    
    # Média de pontuação em quizzes
    quiz_scores = []
    for record in records:
        if record.quiz_scores:
            for quiz in record.quiz_scores:
                if "score" in quiz:
                    quiz_scores.append(quiz["score"])
    
    quiz_average_score = sum(quiz_scores) / len(quiz_scores) if quiz_scores else 0
    
    # Taxa de retenção de flashcards
    flashcard_retention = []
    for record in records:
        if record.flashcard_stats and "retention_rate" in record.flashcard_stats:
            flashcard_retention.append(record.flashcard_stats["retention_rate"])
    
    flashcard_retention_rate = sum(flashcard_retention) / len(flashcard_retention) if flashcard_retention else 0
    
    # Sequência de estudo
    # Implementação simplificada
    study_streak = 5
    
    # Progresso semanal e mensal
    # Implementação simplificada
    weekly_progress = [
        {"week": "Semana 1", "study_time": 300, "quiz_score": 85},
        {"week": "Semana 2", "study_time": 350, "quiz_score": 88},
    ]
    
    monthly_progress = [
        {"month": "Janeiro", "study_time": 1200, "quiz_score": 82},
        {"month": "Fevereiro", "study_time": 1500, "quiz_score": 87},
    ]
    
    return {
        "total_study_time": total_study_time,
        "subject_distribution": subject_distribution,
        "quiz_average_score": quiz_average_score,
        "flashcard_retention_rate": flashcard_retention_rate,
        "study_streak": study_streak,
        "weekly_progress": weekly_progress,
        "monthly_progress": monthly_progress,
    }

@router.get("/{record_id}", response_model=PerformanceRecordSchema)
def read_performance_record(
    *,
    db: Session = Depends(get_db),
    record_id: str,
    current_user: User = Depends(get_current_user),
) -> Any:
    """
    Recupera um registro de desempenho pelo ID.
    """
    record = db.query(PerformanceRecord).filter(
        PerformanceRecord.id == record_id,
        PerformanceRecord.user_id == current_user.id
    ).first()
    
    if not record:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Registro de desempenho não encontrado",
        )
    
    return record

@router.put("/{record_id}", response_model=PerformanceRecordSchema)
def update_performance_record(
    *,
    db: Session = Depends(get_db),
    record_id: str,
    record_in: PerformanceRecordUpdate,
    current_user: User = Depends(get_current_user),
) -> Any:
    """
    Atualiza um registro de desempenho.
    """
    record = db.query(PerformanceRecord).filter(
        PerformanceRecord.id == record_id,
        PerformanceRecord.user_id == current_user.id
    ).first()
    
    if not record:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Registro de desempenho não encontrado",
        )
    
    # Atualizar campos
    if record_in.date is not None:
        record.date = record_in.date
    if record_in.study_time_minutes is not None:
        record.study_time_minutes = record_in.study_time_minutes
    if record_in.subjects_studied is not None:
        record.subjects_studied = record_in.subjects_studied
    if record_in.quiz_scores is not None:
        record.quiz_scores = record_in.quiz_scores
    if record_in.flashcard_stats is not None:
        record.flashcard_stats = record_in.flashcard_stats
    if record_in.notes is not None:
        record.notes = record_in.notes
    
    db.add(record)
    db.commit()
    db.refresh(record)
    return record

@router.delete("/{record_id}", response_model=PerformanceRecordSchema)
def delete_performance_record(
    *,
    db: Session = Depends(get_db),
    record_id: str,
    current_user: User = Depends(get_current_user),
) -> Any:
    """
    Exclui um registro de desempenho.
    """
    record = db.query(PerformanceRecord).filter(
        PerformanceRecord.id == record_id,
        PerformanceRecord.user_id == current_user.id
    ).first()
    
    if not record:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Registro de desempenho não encontrado",
        )
    
    db.delete(record)
    db.commit()
    return record
