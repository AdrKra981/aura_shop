from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from typing import List

from app.core.database import get_db
from app.schemas.product import ProductCreate, ProductRead
from app.services.product import ProductService
from app.core.dependencies import require_admin

router = APIRouter(prefix="/products", tags=["products"])

# Admin-only: create
@router.post(
    "",
    response_model=ProductRead,
    status_code=status.HTTP_201_CREATED,
    dependencies=[Depends(require_admin)]
)
async def create_product(
    data: ProductCreate,
    db: AsyncSession = Depends(get_db)
):
    service = ProductService(db)
    return await service.create_product(data)

# Public: list all
@router.get(
    "",
    response_model=List[ProductRead],
    status_code=status.HTTP_200_OK
)
async def list_products(db: AsyncSession = Depends(get_db)):
    service = ProductService(db)
    return await service.list_products()

# Public: get detail
@router.get(
    "/{product_id}",
    response_model=ProductRead,
    status_code=status.HTTP_200_OK
)
async def get_product(product_id: str, db: AsyncSession = Depends(get_db)):
    service = ProductService(db)
    product = await service.get_product(product_id)
    if not product:
        raise HTTPException(status_code=404, detail="Product not found")
    return product
