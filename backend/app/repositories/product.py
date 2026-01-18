from uuid import UUID
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from app.models.product import Product
from typing import List, Optional, Tuple
from app.schemas.product_query import ProductQueryParams
from sqlalchemy import func

ALLOWED_SORTS = [
    "name",
    "price",
    "created_at",
    "updated_at",
]

class ProductRepository:
    def __init__(self, session: AsyncSession):
        self.session = session

    async def get_all(self) -> List[Product]:
        stmt = select(Product).where(Product.is_active == True)
        result = await self.session.execute(stmt)
        return result.scalars().all()

    async def get_paginated(
    self,
    params: ProductQueryParams,
    ) -> Tuple[list[Product], int]:
        stmt = select(Product).where(Product.is_active == True)

        if params.category_id:
            stmt = stmt.where(Product.category_id == params.category_id)

        if params.min_price is not None:
            stmt = stmt.where(Product.price >= params.min_price)

        if params.max_price is not None:
            stmt = stmt.where(Product.price <= params.max_price)

        if params.search:
            stmt = stmt.where(Product.name.ilike(f"%{params.search}%"))

        sort_column = getattr(Product, params.sort, Product.created_at)
        if sort_column not in ALLOWED_SORTS:
            sort_column = Product.created_at

        if params.order not in ["asc", "desc"]:
            params.order = "asc"

        stmt = stmt.order_by(
            sort_column.asc() if params.order == "asc" else sort_column.desc()
        )

        count_stmt = select(func.count()).select_from(stmt.subquery())
        total = (await self.session.execute(count_stmt)).scalar()

        offset = (params.page - 1) * params.page_size
        stmt = stmt.offset(offset).limit(params.page_size)

        result = await self.session.execute(stmt)
        return result.scalars().all(), total


    async def get_all_admin(self) -> List[Product]:
        stmt = select(Product)
        result = await self.session.execute(stmt)
        return result.scalars().all()

    async def get_by_id(self, product_id: str) -> Optional[Product]:
        stmt = select(Product).where(Product.id == product_id)
        result = await self.session.execute(stmt)
        return result.scalar_one_or_none()

    async def get_by_category(self, category_id):
        result = await self.session.execute(
            select(Product).where(Product.category_id == category_id and Product.is_active == True)
        )
        return result.scalars().all()

    async def create(self, product: Product) -> Product:
        self.session.add(product)
        await self.session.commit()
        await self.session.refresh(product)
        return product

    async def update(self, product_id: str, product: Product) -> Optional[Product]:
        product = await self.get_by_id(product_id)
        if not product:
            return None
        product.name = product.name
        product.description = product.description
        product.price = product.price
        product.category_id = product.category_id
        product.stock = product.stock
        await self.session.commit()
        await self.session.refresh(product)
        return product

    async def delete(self, product_id: str) -> Optional[Product]:
        product = await self.get_by_id(product_id)
        if not product:
            return None
        await self.session.delete(product)
        await self.session.commit()
        return product

    async def get_for_update(self, product_id: UUID) -> Optional[Product]:
        result = await self.session.execute(
            select(Product).where(Product.id == product_id).with_for_update()
        )
        return result.scalar_one_or_none()
