from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from app.core.database import get_db
from app.services.cart import CartService
from app.schemas.cart import (
    AddToCartRequest,
    CartResponse,
)
from app.core.dependencies import get_current_user
from app.models.user import User
from app.modules.cart.cart_mapper import map_cart

router = APIRouter(prefix="/cart", tags=["Cart"])


@router.get("", response_model=CartResponse)
async def get_cart(
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    service = CartService(db)
    cart = await service.cart_repo.get_active_cart(current_user.id)
    if not cart:
        return CartResponse(id=None, items=[])
    return map_cart(cart)


@router.post("/items", response_model=CartResponse)
async def add_to_cart(
    payload: AddToCartRequest,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    service = CartService(db)
    cart = await service.add_to_cart(
        user_id=current_user.id,
        product_id=payload.product_id,
        quantity=payload.quantity,
    )
    return map_cart(cart)


@router.delete("/items/{product_id}", response_model=CartResponse)
async def remove_from_cart(
    product_id: str,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    service = CartService(db)
    await service.remove_from_cart(
        user_id=current_user.id,
        product_id=product_id,
    )
    cart = await service.cart_repo.get_active_cart(current_user.id)
    return map_cart(cart)
