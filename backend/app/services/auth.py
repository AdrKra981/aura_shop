from sqlalchemy.ext.asyncio import AsyncSession

from app.repositories.user import UserRepository
from app.core.security import verify_password, create_access_token


class AuthService:
    def __init__(self, session: AsyncSession):
        self.repo = UserRepository(session)

    async def authenticate(self, email: str, password: str) -> str:
        user = await self.repo.get_by_email(email)
        if not user:
            raise ValueError("Invalid credentials")

        if not verify_password(password, user.hashed_password):
            raise ValueError("Invalid credentials")

        return create_access_token({"sub": str(user.id)})
