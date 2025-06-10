from typing import Generator, Optional

from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from jose import jwt
from pydantic import ValidationError
from sqlalchemy.orm import Session

from app.core.config import settings
from app.core.security import ALGORITHM
from app.db.base import get_db
from app.db.models.user import User
from app.schemas.token import TokenPayload

# OAuth2 scheme para autenticação
oauth2_scheme = OAuth2PasswordBearer(tokenUrl=f"{settings.API_PREFIX}/auth/login")

def get_current_user(
    db: Session = Depends(get_db), token: str = Depends(oauth2_scheme)
) -> User:
    """
    Dependency para obter o usuário atual a partir do token JWT.
    
    Args:
        db: Sessão do banco de dados
        token: Token JWT
        
    Returns:
        Usuário atual
        
    Raises:
        HTTPException: Se o token for inválido ou o usuário não existir
    """
    try:
        payload = jwt.decode(token, settings.SECRET_KEY, algorithms=[ALGORITHM])
        token_data = TokenPayload(**payload)
    except (jwt.JWTError, ValidationError):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Não foi possível validar as credenciais",
            headers={"WWW-Authenticate": "Bearer"},
        )
    
    user = db.query(User).filter(User.id == token_data.sub).first()
    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Usuário não encontrado"
        )
    
    if not user.is_active:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Usuário inativo"
        )
    
    return user

def get_current_active_user(current_user: User = Depends(get_current_user)) -> User:
    """
    Dependency para obter o usuário atual ativo.
    
    Args:
        current_user: Usuário atual
        
    Returns:
        Usuário atual ativo
        
    Raises:
        HTTPException: Se o usuário não estiver ativo
    """
    if not current_user.is_active:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Usuário inativo"
        )
    return current_user

def get_current_admin_user(current_user: User = Depends(get_current_user)) -> User:
    """
    Dependency para obter o usuário atual administrador.
    
    Args:
        current_user: Usuário atual
        
    Returns:
        Usuário atual administrador
        
    Raises:
        HTTPException: Se o usuário não for administrador
    """
    if not current_user.is_admin:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Permissão insuficiente"
        )
    return current_user
