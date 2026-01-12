from pydantic import BaseModel, Field
from typing import Optional

class ProductBase(BaseModel):
    name: str = Field(..., max_length=100)
    description: Optional[str]
    price: float
    stock: int = 0

class ProductCreate(ProductBase):
    pass

class ProductRead(ProductBase):
    id: str
    created_at: Optional[str]
    updated_at: Optional[str]

    class Config:
        from_attributes = True
