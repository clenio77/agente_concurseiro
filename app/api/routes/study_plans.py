from datetime import datetime, timedelta
from typing import Any, List

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.api.deps import get_current_user
from app.db.base import get_db
from app.db.models.study_plan import StudyPlan
from app.db.models.user import User
from app.schemas.study_plan import (
    StudyPlan as StudyPlanSchema,
    StudyPlanCreate,
    StudyPlanUpdate,
)

router = APIRouter()

@router.get("/", response_model=List[StudyPlanSchema])
def read_study_plans(
    db: Session = Depends(get_db),
    skip: int = 0,
    limit: int = 100,
    current_user: User = Depends(get_current_user),
) -> Any:
    """
    Recupera todos os planos de estudo do usuário atual.
    """
    study_plans = (
        db.query(StudyPlan)
        .filter(StudyPlan.user_id == current_user.id)
        .offset(skip)
        .limit(limit)
        .all()
    )
    return study_plans

@router.post("/", response_model=StudyPlanSchema)
def create_study_plan(
    *,
    db: Session = Depends(get_db),
    study_plan_in: StudyPlanCreate,
    current_user: User = Depends(get_current_user),
) -> Any:
    """
    Cria um novo plano de estudos.
    """
    # Definir data de início se não fornecida
    start_date = study_plan_in.start_date or datetime.utcnow()
    
    # Calcular data de término
    end_date = start_date + timedelta(days=30 * study_plan_in.duration_months)
    
    # Criar plano de estudos
    study_plan = StudyPlan(
        user_id=current_user.id,
        title=study_plan_in.title,
        description=study_plan_in.description,
        cargo=study_plan_in.cargo,
        concurso=study_plan_in.concurso,
        banca=study_plan_in.banca,
        cidade=study_plan_in.cidade,
        study_hours_per_week=study_plan_in.study_hours_per_week,
        duration_months=study_plan_in.duration_months,
        start_date=start_date,
        end_date=end_date,
        content=study_plan_in.content,
        is_active=study_plan_in.is_active,
    )
    db.add(study_plan)
    db.commit()
    db.refresh(study_plan)
    return study_plan

@router.get("/{study_plan_id}", response_model=StudyPlanSchema)
def read_study_plan(
    *,
    db: Session = Depends(get_db),
    study_plan_id: str,
    current_user: User = Depends(get_current_user),
) -> Any:
    """
    Recupera um plano de estudos pelo ID.
    """
    study_plan = db.query(StudyPlan).filter(
        StudyPlan.id == study_plan_id,
        StudyPlan.user_id == current_user.id
    ).first()
    
    if not study_plan:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Plano de estudos não encontrado",
        )
    
    return study_plan

@router.put("/{study_plan_id}", response_model=StudyPlanSchema)
def update_study_plan(
    *,
    db: Session = Depends(get_db),
    study_plan_id: str,
    study_plan_in: StudyPlanUpdate,
    current_user: User = Depends(get_current_user),
) -> Any:
    """
    Atualiza um plano de estudos.
    """
    study_plan = db.query(StudyPlan).filter(
        StudyPlan.id == study_plan_id,
        StudyPlan.user_id == current_user.id
    ).first()
    
    if not study_plan:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Plano de estudos não encontrado",
        )
    
    # Atualizar campos
    if study_plan_in.title is not None:
        study_plan.title = study_plan_in.title
    if study_plan_in.description is not None:
        study_plan.description = study_plan_in.description
    if study_plan_in.cargo is not None:
        study_plan.cargo = study_plan_in.cargo
    if study_plan_in.concurso is not None:
        study_plan.concurso = study_plan_in.concurso
    if study_plan_in.banca is not None:
        study_plan.banca = study_plan_in.banca
    if study_plan_in.cidade is not None:
        study_plan.cidade = study_plan_in.cidade
    if study_plan_in.study_hours_per_week is not None:
        study_plan.study_hours_per_week = study_plan_in.study_hours_per_week
    if study_plan_in.duration_months is not None:
        study_plan.duration_months = study_plan_in.duration_months
        # Recalcular data de término
        study_plan.end_date = study_plan.start_date + timedelta(days=30 * study_plan.duration_months)
    if study_plan_in.content is not None:
        study_plan.content = study_plan_in.content
    if study_plan_in.is_active is not None:
        study_plan.is_active = study_plan_in.is_active
    
    study_plan.updated_at = datetime.utcnow()
    
    db.add(study_plan)
    db.commit()
    db.refresh(study_plan)
    return study_plan

@router.delete("/{study_plan_id}", response_model=StudyPlanSchema)
def delete_study_plan(
    *,
    db: Session = Depends(get_db),
    study_plan_id: str,
    current_user: User = Depends(get_current_user),
) -> Any:
    """
    Exclui um plano de estudos.
    """
    study_plan = db.query(StudyPlan).filter(
        StudyPlan.id == study_plan_id,
        StudyPlan.user_id == current_user.id
    ).first()
    
    if not study_plan:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Plano de estudos não encontrado",
        )
    
    db.delete(study_plan)
    db.commit()
    return study_plan
