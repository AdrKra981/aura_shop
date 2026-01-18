from app.schemas.category import CategoryUpdate
from uuid import UUID
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from typing import List

from app.schemas.category import CategoryCreate, CategoryRead
from app.services.category import CategoryService
from app.core.dependencies import require_admin
from app.core.database import get_db

router = APIRouter(prefix="/categories", tags=["categories"])

# Admin-only: create category
@router.post(
    "",
    response_model=CategoryRead,
    status_code=status.HTTP_201_CREATED,
    dependencies=[Depends(require_admin)]
)
async def create_category(
    data: CategoryCreate,
    db: AsyncSession = Depends(get_db)
):
    service = CategoryService(db)
    return await service.create_category(data)

# Public: list all categories
@router.get(
    "",
    response_model=List[CategoryRead],
    status_code=status.HTTP_200_OK
)
async def list_categories(db: AsyncSession = Depends(get_db)):
    service = CategoryService(db)
    return await service.list_categories()

# Public: get category detail
@router.get(
    "/{category_id}",
    response_model=CategoryRead,
    status_code=status.HTTP_200_OK
)
async def get_category(category_id: str, db: AsyncSession = Depends(get_db)):
    service = CategoryService(db)
    category = await service.get_category(category_id)
    if not category:
        raise HTTPException(status_code=404, detail="Category not found")
    return category

@router.post(
    "/",
    response_model=CategoryRead,
    status_code=status.HTTP_201_CREATED,
    dependencies=[Depends(require_admin)],
)
async def create_category(
    data: CategoryCreate,
    session: AsyncSession = Depends(get_db),
):
    service = CategoryService(session)
    return await service.create(data)   

@router.put(
    "/{category_id}",
    response_model=CategoryRead,
    dependencies=[Depends(require_admin)],
)
async def update_category(
    category_id: UUID,
    data: CategoryUpdate,
    session: AsyncSession = Depends(get_db),
):
    service = CategoryService(session)
    try:
        return await service.update(category_id, data)
    except ValueError:
        raise HTTPException(status_code=404, detail="Category not found")

@router.delete(
    "/{category_id}",
    status_code=status.HTTP_204_NO_CONTENT,
    dependencies=[Depends(require_admin)],
)
async def delete_category(
    category_id: UUID,
    session: AsyncSession = Depends(get_db),
):
    service = CategoryService(session)
    try:
        await service.delete(category_id)
    except ValueError:
        raise HTTPException(status_code=404, detail="Category not found")


