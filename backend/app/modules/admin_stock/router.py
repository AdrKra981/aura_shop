from app.core.database import get_db
from fastapi import Depends
from app.core.dependencies import require_admin
from fastapi import APIRouter
from app.services.stock import StockService
from app.repositories.product import ProductRepository
from sqlalchemy.ext.asyncio import AsyncSession
from uuid import UUID
from fastapi import HTTPException

router = APIRouter(
    prefix="/admin/stock",
    tags=["Admin Stock"],
    dependencies=[
        Depends(require_admin)
    ]
)

@router.put("/{product_id}")
async def set_stock(product_id: UUID, quantity: int, session: AsyncSession = Depends(get_db)):
    service = StockService(session)
    try:
        return await service.set_stock(product_id, quantity)
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

@router.post("/{product_id}/adjust")
async def adjust_stock(product_id: UUID, delta: int, session: AsyncSession = Depends(get_db)):
    service = StockService(session)
    try:
        return await service.adjust_stock(product_id, delta)
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))