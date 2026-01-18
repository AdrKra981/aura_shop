from fastapi import HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from app.repositories.product import ProductRepository
from uuid import UUID

class StockService:
    def __init__(self, session: AsyncSession):
        self.repo = ProductRepository(session)
        self.session = session

    async def set_stock(self, product_id: UUID, quantity: int):
        product = await self.repo.get_for_update(product_id)
        if not product:
            raise HTTPException(status_code=404, detail="Product not found")
        product.stock = quantity
        await self.session.commit()
        await self.session.refresh(product)
        return product

    async def adjust_stock(self, product_id: UUID, delta: int):
        product = await self.repo.get_for_update(product_id)
        if not product:
            raise HTTPException(status_code=404, detail="Product not found")
        product.stock += delta
        await self.session.commit()
        await self.session.refresh(product)
        return product
          