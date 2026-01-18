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
    pass

class ProductRead(BaseModel):
    id: UUID
    name: str
    description: str | None
    price: int
    stock: int
    category_id: UUID

    class Config:
        from_attributes = True
