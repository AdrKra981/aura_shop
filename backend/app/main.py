from fastapi import Depends, FastAPI
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import text

from app.core.database import get_db
from app.modules.users.router import router as users_router
from app.modules.auth.router import router as auth_router
from app.modules.products.router import router as products_router
from app.modules.categories.router import router as categories_router

app = FastAPI(title="Aura Shop API")

app.include_router(users_router)
app.include_router(auth_router)
app.include_router(products_router)
app.include_router(categories_router)

@app.get("/health")
def health_check():
    return {"status": "ok"}

@app.get("/health/db")
async def db_health_check(db: AsyncSession = Depends(get_db)):
    result = await db.execute(text("SELECT 1"))
    return {"db": result.scalar()}