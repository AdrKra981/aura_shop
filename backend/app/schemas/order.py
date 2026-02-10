from pydantic import BaseModel
from uuid import UUID
from decimal import Decimal
from typing import List
from datetime import datetime
from app.models.order import OrderStatus


class OrderItemResponse(BaseModel):
    product_name: str
    product_price: Decimal
    quantity: int

    class Config:
        from_attributes = True


class OrderResponse(BaseModel):
    id: UUID
    status: OrderStatus
    total_price: Decimal
    created_at: datetime
    items: List[OrderItemResponse]

    class Config:
        from_attributes = True
