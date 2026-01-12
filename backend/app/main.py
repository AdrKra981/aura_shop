from fastapi import Depends, FastAPI
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import text

from app.core.database import get_db
from app.modules.users.router import router as users_router

app = FastAPI(title="Aura Shop API")

app.include_router(users_router)

@app.get("/health")
def health_check():
    return {"status": "ok"}

@app.get("/health/db")
async def db_health_check(db: AsyncSession = Depends(get_db)):
    result = await db.execute(text("SELECT 1"))
    return {"db": result.scalar()}