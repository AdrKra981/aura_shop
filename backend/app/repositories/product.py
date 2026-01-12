from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from app.models.product import Product
from typing import List, Optional

class ProductRepository:
    def __init__(self, session: AsyncSession):
        self.session = session

    async def get_all(self) -> List[Product]:
        stmt = select(Product)
        result = await self.session.execute(stmt)
        return result.scalars().all()

    async def get_by_id(self, product_id: str) -> Optional[Product]:
        stmt = select(Product).where(Product.id == product_id)
        result = await self.session.execute(stmt)
        return result.scalar_one_or_none()

    async def create(self, product: Product) -> Product:
        self.session.add(product)
        await self.session.commit()
        await self.session.refresh(product)
        return product
