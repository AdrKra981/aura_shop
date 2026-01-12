from app.models.user import UserRole
import uuid
from datetime import datetime

from pydantic import BaseModel, EmailStr, Field


class UserBase(BaseModel):
    email: EmailStr


class UserCreate(UserBase):
    password: str = Field(min_length=8)


class UserRead(UserBase):
    id: uuid.UUID
    is_active: bool
    is_admin: bool
    role: UserRole
    created_at: datetime

    class Config:
        from_attributes = True
