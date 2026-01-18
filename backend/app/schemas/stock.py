from pydantic import BaseModel, Field

class StockUpdate(BaseModel):
    stock: int = Field(..., ge=0)

class StockAdjust(BaseModel):
    delta: int