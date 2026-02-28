from fastapi import Header
from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.database import get_db
from app.services.checkout import CheckoutService
from app.core.dependencies import get_current_user
from app.models.user import User

router = APIRouter(prefix="/checkout", tags=["Checkout"])


@router.post("")
async def checkout(
    idempotency_key: str | None = Header(default=None),
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    service = CheckoutService(db)
    return await service.checkout(
        user_id=current_user.id,
        idempotency_key=idempotency_key,
    )
