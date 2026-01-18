from app.schemas.pagination import PaginatedResponse
from app.schemas.product import ProductUpdate
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from typing import List

from app.core.database import get_db
from app.schemas.product import ProductCreate, ProductRead
from app.services.product import ProductService
from app.core.dependencies import require_admin
from app.schemas.product_query import ProductQueryParams

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
    response_model=PaginatedResponse[ProductRead],
    status_code=status.HTTP_200_OK
)
async def list_products(db: AsyncSession = Depends(get_db), params: ProductQueryParams = Depends(ProductQueryParams)):
    service = ProductService(db)
    return await service.list_products(params)

# Admin-only: list all
@router.get(
    "/admin",
    response_model=PaginatedResponse[ProductRead],
    status_code=status.HTTP_200_OK,
    dependencies=[Depends(require_admin)]
)
async def list_products_admin(db: AsyncSession = Depends(get_db), params: ProductQueryParams = Depends(ProductQueryParams)):
    service = ProductService(db)
    return await service.list_products_admin(params)

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

@router.put(
    "/{product_id}",
    response_model=ProductRead,
    status_code=status.HTTP_200_OK,
    dependencies=[Depends(require_admin)]
)
async def update_product(
    product_id: str,
    data: ProductUpdate,
    db: AsyncSession = Depends(get_db)
):
    service = ProductService(db)
    product = await service.update_product(product_id, data)
    if not product:
        raise HTTPException(status_code=404, detail="Product not found")
    return product

@router.delete(
    "/{product_id}",
    status_code=status.HTTP_204_NO_CONTENT,
    dependencies=[Depends(require_admin)]
)
async def delete_product(product_id: str, db: AsyncSession = Depends(get_db)):
    service = ProductService(db)
    product = await service.delete_product(product_id)
    if not product:
        raise HTTPException(status_code=404, detail="Product not found")
    return product
