from pydantic import BaseModel, Field
from typing import Optional, List
from app.schemas.product import ProductRead
from uuid import UUID

class CategoryBase(BaseModel):
    name: str = Field(..., max_length=100)

class CategoryCreate(BaseModel):
    name: str
    description: str | None = None


class CategoryUpdate(BaseModel):
    name: str | None = None
    description: str | None = None

class CategoryRead(CategoryBase):
    id: UUID
    name: str
    description: str | None

    class Config:
        from_attributes = True
