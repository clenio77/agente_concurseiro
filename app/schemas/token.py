from typing import Optional
from pydantic import BaseModel, UUID4

class Token(BaseModel):
    """Esquema para token de acesso."""
    access_token: str
    token_type: str = "bearer"

class TokenPayload(BaseModel):
    """Esquema para payload do token JWT."""
    sub: Optional[str] = None
    exp: Optional[int] = None

class TokenData(BaseModel):
    """Esquema para dados do token."""
    user_id: UUID4