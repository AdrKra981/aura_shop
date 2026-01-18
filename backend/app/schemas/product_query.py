from pydantic import BaseModel, Field
from uuid import UUID


class ProductQueryParams(BaseModel):
    page: int = Field(default=1, ge=1)
    page_size: int = Field(default=20, ge=1, le=100)

    category_id: UUID | None = None
    min_price: int | None = None
    max_price: int | None = None
    search: str | None = None

    sort: str = "created_at"
    order: str = "desc"
