from uuid import UUID
from sqlalchemy.ext.asyncio import AsyncSession
from app.models.product import Product
from app.schemas.product import ProductCreate, ProductUpdate
from app.repositories.product import ProductRepository
from app.schemas.product_query import ProductQueryParams
from app.schemas.pagination import PaginatedResponse

class ProductService:
    def __init__(self, session: AsyncSession):
        self.repo = ProductRepository(session)

    async def list_products(self, params: ProductQueryParams):
        products, total = await self.repo.get_paginated(params)
        return PaginatedResponse(
            data=products,
            total=total,
            page=params.page,
            page_size=params.page_size,
        )
    
    async def list_products_admin(self):
        return await self.repo.get_all_admin()

    async def get_product(self, product_id: UUID):
        return await self.repo.get_by_id(product_id)

    async def create_product(self, data: ProductCreate):
        product = Product(**data.dict())
        return await self.repo.create(product)

    async def update_product(self, product_id: UUID, data: ProductUpdate):
        product = await self.repo.get_by_id(product_id)
        if not product:
            return None
        product.name = data.name
        product.description = data.description
        product.price = data.price
        product.category_id = data.category_id
        product.stock = data.stock
        return await self.repo.update(product_id, product)

    async def delete_product(self, product_id: UUID):
        product = await self.repo.get_by_id(product_id)
        if not product:
            return None
        product.is_active = False
        return await self.repo.update(product_id, product)

        
