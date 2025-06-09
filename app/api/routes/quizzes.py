from datetime import datetime
from typing import Any, List

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.api.deps import get_current_user
from app.db.base import get_db
from app.db.models.quiz import Quiz, QuizQuestion
from app.db.models.study_plan import StudyPlan
from app.db.models.user import User
from app.schemas.quiz import (
    Quiz as QuizSchema,
    QuizCreate,
    QuizResult,
    QuizUpdate,
)

router = APIRouter()

@router.get("/", response_model=List[QuizSchema])
def read_quizzes(
    db: Session = Depends(get_db),
    skip: int = 0,
    limit: int = 100,
    current_user: User = Depends(get_current_user),
) -> Any:
    """
    Recupera todos os quizzes do usuário atual.
    """
    quizzes = (
        db.query(Quiz)
        .filter(Quiz.user_id == current_user.id)
        .offset(skip)
        .limit(limit)
        .all()
    )
    return quizzes

@router.post("/", response_model=QuizSchema)
def create_quiz(
    *,
    db: Session = Depends(get_db),
    quiz_in: QuizCreate,
    current_user: User = Depends(get_current_user),
) -> Any:
    """
    Cria um novo quiz.
    """
    # Verificar se o plano de estudos existe
    if quiz_in.study_plan_id:
        study_plan = db.query(StudyPlan).filter(
            StudyPlan.id == quiz_in.study_plan_id,
            StudyPlan.user_id == current_user.id
        ).first()
        if not study_plan:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Plano de estudos não encontrado",
            )
    
    # Criar quiz
    quiz = Quiz(
        user_id=current_user.id,
        study_plan_id=quiz_in.study_plan_id,
        title=quiz_in.title,
        description=quiz_in.description,
        difficulty=quiz_in.difficulty,
        subjects=quiz_in.subjects,
        is_completed=False,
    )
    db.add(quiz)
    db.commit()
    db.refresh(quiz)
    
    # Criar questões
    for question_in in quiz_in.questions:
        question = QuizQuestion(
            quiz_id=quiz.id,
            text=question_in.text,
            options=question_in.options,
            correct_answer=question_in.correct_answer,
            explanation=question_in.explanation,
            subject=question_in.subject,
            difficulty=question_in.difficulty,
        )
        db.add(question)
    
    db.commit()
    db.refresh(quiz)
    return quiz

@router.get("/{quiz_id}", response_model=QuizSchema)
def read_quiz(
    *,
    db: Session = Depends(get_db),
    quiz_id: str,
    current_user: User = Depends(get_current_user),
) -> Any:
    """
    Recupera um quiz pelo ID.
    """
    quiz = db.query(Quiz).filter(
        Quiz.id == quiz_id,
        Quiz.user_id == current_user.id
    ).first()
    
    if not quiz:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Quiz não encontrado",
        )
    
    return quiz

@router.post("/{quiz_id}/submit", response_model=QuizSchema)
def submit_quiz(
    *,
    db: Session = Depends(get_db),
    quiz_id: str,
    quiz_result: QuizResult,
    current_user: User = Depends(get_current_user),
) -> Any:
    """
    Submete respostas para um quiz.
    """
    quiz = db.query(Quiz).filter(
        Quiz.id == quiz_id,
        Quiz.user_id == current_user.id
    ).first()
    
    if not quiz:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Quiz não encontrado",
        )
    
    if quiz.is_completed:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Quiz já foi completado",
        )
    
    # Processar respostas
    correct_answers = 0
    total_questions = len(quiz.questions)
    
    for answer in quiz_result.answers:
        question = db.query(QuizQuestion).filter(
            QuizQuestion.id == answer.question_id,
            QuizQuestion.quiz_id == quiz.id
        ).first()
        
        if not question:
            continue
        
        # Atualizar resposta do usuário
        question.user_answer = answer.answer
        question.time_spent_seconds = answer.time_spent_seconds
        question.is_correct = question.correct_answer == answer.answer
        
        if question.is_correct:
            correct_answers += 1
        
        db.add(question)
    
    # Atualizar quiz
    quiz.is_completed = True
    quiz.score = (correct_answers / total_questions) * 100 if total_questions > 0 else 0
    quiz.completed_at = datetime.utcnow()
    
    if not quiz.started_at:
        quiz.started_at = datetime.utcnow()
    
    db.add(quiz)
    db.commit()
    db.refresh(quiz)
    return quiz

@router.delete("/{quiz_id}", response_model=QuizSchema)
def delete_quiz(
    *,
    db: Session = Depends(get_db),
    quiz_id: str,
    current_user: User = Depends(get_current_user),
) -> Any:
    """
    Exclui um quiz.
    """
    quiz = db.query(Quiz).filter(
        Quiz.id == quiz_id,
        Quiz.user_id == current_user.id
    ).first()
    
    if not quiz:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Quiz não encontrado",
        )
    
    db.delete(quiz)
    db.commit()
    return quiz
