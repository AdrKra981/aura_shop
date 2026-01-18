from uuid import UUID
from app.schemas.category import CategoryUpdate
from sqlalchemy.ext.asyncio import AsyncSession
from app.models.category import Category
from app.schemas.category import CategoryCreate
from app.repositories.category import CategoryRepository

class CategoryService:
    def __init__(self, session: AsyncSession):
        self.repo = CategoryRepository(session)
        self.session = session

    async def list_categories(self):
        return await self.repo.get_all()

    async def get_category(self, category_id: str):
        return await self.repo.get_by_id(category_id)

    async def create(self, data: CategoryCreate) -> Category:
        category = Category(**data.model_dump())
        self.repo.add(category)
        await self.session.commit()
        await self.session.refresh(category)
        return category

    async def update(self, category_id: UUID, data: CategoryUpdate) -> Category:
        category = await self.repo.get_by_id(category_id)
        if not category:
            raise ValueError("Category not found")

        for field, value in data.model_dump(exclude_unset=True).items():
            setattr(category, field, value)

        await self.session.commit()
        await self.session.refresh(category)
        return category

    async def delete(self, category_id: UUID) -> None:
        category = await self.repo.get_by_id(category_id)
        if not category:
            raise ValueError("Category not found")

        await self.session.delete(category)
        await self.session.commit()
