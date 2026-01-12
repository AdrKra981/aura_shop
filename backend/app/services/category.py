from sqlalchemy.ext.asyncio import AsyncSession
from app.models.category import Category
from app.schemas.category import CategoryCreate
from app.repositories.category import CategoryRepository

class CategoryService:
    def __init__(self, session: AsyncSession):
        self.repo = CategoryRepository(session)

    async def list_categories(self):
        return await self.repo.get_all()

    async def get_category(self, category_id: str):
        return await self.repo.get_by_id(category_id)

    async def create_category(self, data: CategoryCreate):
        category = Category(**data.dict())
        return await self.repo.create(category)
