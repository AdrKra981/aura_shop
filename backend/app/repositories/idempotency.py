from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from app.models.idempotency_key import IdempotencyKey


class IdempotencyRepository:
    def __init__(self, session: AsyncSession):
        self.session = session

    async def get(self, key: str) -> IdempotencyKey | None:
        result = await self.session.execute(
            select(IdempotencyKey).where(IdempotencyKey.key == key)
        )
        return result.scalar_one_or_none()

    async def save(self, key: str, response_body: str):
        record = IdempotencyKey(
            key=key,
            response_body=response_body,
        )
        self.session.add(record)
