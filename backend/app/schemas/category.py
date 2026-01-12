from pydantic import BaseModel, Field
from typing import Optional, List
from app.schemas.product import ProductRead

class CategoryBase(BaseModel):
    name: str = Field(..., max_length=100)

class CategoryCreate(CategoryBase):
    pass

class CategoryRead(CategoryBase):
    id: str
    products: Optional[List[ProductRead]] = []

    class Config:
        from_attributes = True
