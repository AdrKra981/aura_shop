from pydantic import BaseModel
from uuid import UUID
from typing import List
from decimal import Decimal


class CartItemResponse(BaseModel):
    product_id: UUID
    product_name: str
    product_price: Decimal
    quantity: int

    class Config:
        from_attributes = True


class CartResponse(BaseModel):
    id: UUID
    items: List[CartItemResponse]

    class Config:
        from_attributes = True


class AddToCartRequest(BaseModel):
    product_id: UUID
    quantity: int
