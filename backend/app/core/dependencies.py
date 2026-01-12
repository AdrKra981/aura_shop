import uuid

from fastapi import Depends, HTTPException, status
from fastapi.security import APIKeyHeader
from jose import jwt, JWTError
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.database import get_db
from app.core.config import settings
from app.repositories.user import UserRepository
from app.models.user import User, UserRole

auth_header = APIKeyHeader(name="Authorization")

async def get_current_user(
    token: str = Depends(auth_header),
    db: AsyncSession = Depends(get_db),
):
    if not token.startswith("Bearer "):
        raise HTTPException(status_code=401)
    token_value = token[len("Bearer "):]
    try:
        payload = jwt.decode(
            token_value,
            settings.SECRET_KEY,
            algorithms=[settings.ALGORITHM],
        )
        user_id: str | None = payload.get("sub")
        if user_id is None:
            raise HTTPException(status_code=401)
    except JWTError:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid token",
        )

    repo = UserRepository(db)
    user = await repo.get_by_id(uuid.UUID(user_id))

    if user is None:
        raise HTTPException(status_code=401, detail="User not found")

    return user

def require_admin(current_user: User = Depends(get_current_user)):
    if current_user.role != UserRole.ADMIN:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Admin access required"
        )
    return current_user