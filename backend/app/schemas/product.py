from pydantic import BaseModel, Field
from typing import Optional
from uuid import UUID

class ProductBase(BaseModel):
    name: str = Field(..., max_length=100)
    description: Optional[str]
    price: float
    category_id: str
    stock: int = 0

class ProductCreate(ProductBase):
    name: str 
    description: Optional[str]
    price: int
    category_id: UUID
    stock: int = 0

class ProductRead(BaseModel):
    id: UUID
    name: str
    description: str | None
    price: int
    stock: int
    category_id: UUID

    class Config:
        from_attributes = True

class ProductUpdate(BaseModel):
    name: str | None = None
    description: str | None = None
    price: int | None = None
    stock: int | None = None
    category_id: UUID | None = None
    is_active: bool | None = None
