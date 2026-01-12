from sqlalchemy.ext.asyncio import AsyncSession
from app.models.product import Product
from app.schemas.product import ProductCreate
from app.repositories.product import ProductRepository

class ProductService:
    def __init__(self, session: AsyncSession):
        self.repo = ProductRepository(session)

    async def list_products(self):
        return await self.repo.get_all()

    async def get_product(self, product_id: str):
        return await self.repo.get_by_id(product_id)

    async def create_product(self, data: ProductCreate):
        product = Product(**data.dict())
        return await self.repo.create(product)
