from sqlalchemy.ext.asyncio import AsyncSession

from app.repositories.user import UserRepository
from app.schemas.user import UserCreate
from app.core.security import hash_password


class UserService:
    def __init__(self, session: AsyncSession):
        self.repo = UserRepository(session)

    async def create_user(self, data: UserCreate):
        hashed_password = hash_password(data.password)

        return await self.repo.create(
            email=data.email,
            hashed_password=hashed_password,
        )
