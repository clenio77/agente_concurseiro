"""
Rotas de flashcards da API.
Inclui endpoints para CRUD, revisão e listagem de flashcards do usuário.
"""

from datetime import datetime, timedelta
from typing import Any, List

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.api.deps import get_current_user
from app.db.base import get_db
from app.db.models.flashcard import Flashcard, FlashcardReview
from app.db.models.user import User
from app.schemas.flashcard import (
    Flashcard as FlashcardSchema,
    FlashcardCreate,
    FlashcardReviewCreate,
    FlashcardUpdate,
)

router = APIRouter()

@router.get("/", response_model=List[FlashcardSchema])
def read_flashcards(
    db: Session = Depends(get_db),
    skip: int = 0,
    limit: int = 100,
    subject: str = None,
    current_user: User = Depends(get_current_user),
) -> Any:
    """
    Recupera todos os flashcards do usuário atual.
    Permite filtrar por matéria (subject) e paginar resultados.
    """
    query = db.query(Flashcard).filter(Flashcard.user_id == current_user.id)
    
    if subject:
        query = query.filter(Flashcard.subject == subject)
    
    flashcards = query.offset(skip).limit(limit).all()
    return flashcards

@router.post("/", response_model=FlashcardSchema)
def create_flashcard(
    *,
    db: Session = Depends(get_db),
    flashcard_in: FlashcardCreate,
    current_user: User = Depends(get_current_user),
) -> Any:
    """
    Cria um novo flashcard para o usuário autenticado.
    """
    flashcard = Flashcard(
        user_id=current_user.id,
        front=flashcard_in.front,
        back=flashcard_in.back,
        subject=flashcard_in.subject,
        difficulty=flashcard_in.difficulty,
    )
    db.add(flashcard)
    db.commit()
    db.refresh(flashcard)
    return flashcard

@router.get("/due", response_model=List[FlashcardSchema])
def read_due_flashcards(
    db: Session = Depends(get_db),
    limit: int = 20,
    current_user: User = Depends(get_current_user),
) -> Any:
    """
    Recupera flashcards que estão prontos para revisão (baseado em next_review).
    """
    now = datetime.utcnow()
    flashcards = (
        db.query(Flashcard)
        .filter(Flashcard.user_id == current_user.id)
        .filter(Flashcard.next_review <= now)
        .order_by(Flashcard.next_review)
        .limit(limit)
        .all()
    )
    return flashcards

@router.post("/{flashcard_id}/review", response_model=FlashcardSchema)
def review_flashcard(
    *,
    db: Session = Depends(get_db),
    flashcard_id: str,
    review_in: FlashcardReviewCreate,
    current_user: User = Depends(get_current_user),
) -> Any:
    """
    Registra uma revisão de flashcard e atualiza o algoritmo de repetição espaçada (SM-2).
    - Se a qualidade for menor que 3, reseta o intervalo.
    - Caso contrário, aumenta o intervalo e ajusta o fator de facilidade.
    """
    flashcard = db.query(Flashcard).filter(
        Flashcard.id == flashcard_id,
        Flashcard.user_id == current_user.id
    ).first()
    
    if not flashcard:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Flashcard não encontrado",
        )
    
    # Registrar revisão
    review = FlashcardReview(
        flashcard_id=flashcard.id,
        quality=review_in.quality,
    )
    db.add(review)
    
    # Atualizar algoritmo de repetição espaçada (SM-2)
    if review_in.quality < 3:
        # Se a qualidade for menor que 3, resetar o intervalo
        flashcard.interval = 1
        flashcard.ease_factor = max(1.3, flashcard.ease_factor - 0.2)
    else:
        # Caso contrário, aumentar o intervalo
        if flashcard.interval == 1:
            flashcard.interval = 6
        elif flashcard.interval == 6:
            flashcard.interval = 1 * flashcard.ease_factor
        else:
            flashcard.interval = flashcard.interval * flashcard.ease_factor
        
        # Ajustar o fator de facilidade
        flashcard.ease_factor = flashcard.ease_factor + (0.1 - (5 - review_in.quality) * (0.08 + (5 - review_in.quality) * 0.02))
        if flashcard.ease_factor < 1.3:
            flashcard.ease_factor = 1.3
    
    # Atualizar próxima revisão
    flashcard.next_review = datetime.utcnow() + timedelta(days=int(flashcard.interval))
    
    db.add(flashcard)
    db.commit()
    db.refresh(flashcard)
    return flashcard

@router.get("/{flashcard_id}", response_model=FlashcardSchema)
def read_flashcard(
    *,
    db: Session = Depends(get_db),
    flashcard_id: str,
    current_user: User = Depends(get_current_user),
) -> Any:
    """
    Recupera um flashcard pelo ID do usuário autenticado.
    """
    flashcard = db.query(Flashcard).filter(
        Flashcard.id == flashcard_id,
        Flashcard.user_id == current_user.id
    ).first()
    
    if not flashcard:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Flashcard não encontrado",
        )
    
    return flashcard

@router.put("/{flashcard_id}", response_model=FlashcardSchema)
def update_flashcard(
    *,
    db: Session = Depends(get_db),
    flashcard_id: str,
    flashcard_in: FlashcardUpdate,
    current_user: User = Depends(get_current_user),
) -> Any:
    """
    Atualiza um flashcard do usuário autenticado.
    """
    flashcard = db.query(Flashcard).filter(
        Flashcard.id == flashcard_id,
        Flashcard.user_id == current_user.id
    ).first()
    
    if not flashcard:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Flashcard não encontrado",
        )
    
    # Atualizar campos
    if flashcard_in.front is not None:
        flashcard.front = flashcard_in.front
    if flashcard_in.back is not None:
        flashcard.back = flashcard_in.back
    if flashcard_in.subject is not None:
        flashcard.subject = flashcard_in.subject
    if flashcard_in.difficulty is not None:
        flashcard.difficulty = flashcard_in.difficulty
    
    flashcard.updated_at = datetime.utcnow()
    
    db.add(flashcard)
    db.commit()
    db.refresh(flashcard)
    return flashcard

@router.delete("/{flashcard_id}", response_model=FlashcardSchema)
def delete_flashcard(
    *,
    db: Session = Depends(get_db),
    flashcard_id: str,
    current_user: User = Depends(get_current_user),
) -> Any:
    """
    Exclui um flashcard do usuário autenticado.
    """
    flashcard = db.query(Flashcard).filter(
        Flashcard.id == flashcard_id,
        Flashcard.user_id == current_user.id
    ).first()
    
    if not flashcard:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Flashcard não encontrado",
        )
    
    db.delete(flashcard)
    db.commit()
    return flashcard
