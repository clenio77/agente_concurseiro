from datetime import timedelta
from typing import Any

from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session

from app.api.deps import get_current_user
from app.core.config import settings
from app.core.security import create_access_token, verify_password
from app.db.base import get_db
from app.db.models.user import User
from app.schemas.token import Token
from app.schemas.user import User as UserSchema

router = APIRouter()

@router.post("/login", response_model=Token)
def login_access_token(
    db: Session = Depends(get_db), form_data: OAuth2PasswordRequestForm = Depends()
) -> Any:
    """
    Obtém um token de acesso OAuth2 para autenticação.
    """
    # Buscar usuário pelo nome de usuário
    user = db.query(User).filter(User.username == form_data.username).first()
    
    # Verificar se o usuário existe e a senha está correta
    if not user or not verify_password(form_data.password, user.hashed_password):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Nome de usuário ou senha incorretos",
            headers={"WWW-Authenticate": "Bearer"},
        )
    
    # Verificar se o usuário está ativo
    if not user.is_active:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Usuário inativo"
        )
    
    # Criar token de acesso
    access_token_expires = timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)
    return {
        "access_token": create_access_token(user.id, expires_delta=access_token_expires),
        "token_type": "bearer",
    }

@router.post("/test-token", response_model=UserSchema)
def test_token(current_user: User = Depends(get_current_user)) -> Any:
    """
    Testa se o token de acesso é válido.
    """
    return current_user
