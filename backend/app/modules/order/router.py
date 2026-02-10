from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from uuid import UUID

from app.core.database import get_db
from app.repositories.order import OrderRepository
from app.schemas.order import OrderResponse
from app.core.dependencies import get_current_user, require_admin
from app.models.user import User

router = APIRouter(prefix="/orders", tags=["Orders"])

@router.get("/me", response_model=list[OrderResponse])
async def get_my_orders(
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    repo = OrderRepository(db)
    return await repo.get_by_user(current_user.id)

@router.get("/{order_id}", response_model=OrderResponse)
async def get_order(
    order_id: UUID,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    repo = OrderRepository(db)
    order = await repo.get_by_id(order_id)
    if not order:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Order not found",
        )
    if order.user_id != current_user.id and not current_user.is_admin:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="You don't have permission to access this order",
        )
    return order

@router.get(
    "/admin/all",
    response_model=list[OrderResponse],
    dependencies=[Depends(require_admin)],
)
async def get_all_orders(
    db: AsyncSession = Depends(get_db),
):
    repo = OrderRepository(db)
    return await repo.get_all()