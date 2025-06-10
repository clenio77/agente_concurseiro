from datetime import datetime
from typing import Optional
from uuid import UUID

from pydantic import BaseModel, EmailStr

class UserBase(BaseModel):
    """
    Schema base para usuário.
    """
    email: Optional[EmailStr] = None
    username: Optional[str] = None
    full_name: Optional[str] = None
    is_active: Optional[bool] = True
    is_admin: bool = False

class UserCreate(UserBase):
    """
    Schema para criação de usuário.
    """
    email: EmailStr
    username: str
    password: str

class UserUpdate(UserBase):
    """
    Schema para atualização de usuário.
    """
    password: Optional[str] = None

class User(UserBase):
    """
    Schema para usuário.
    """
    id: UUID
    created_at: datetime
    updated_at: datetime
    
    class Config:
        orm_mode = True
