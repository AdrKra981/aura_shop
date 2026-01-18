from sqlalchemy import Integer
from sqlalchemy import ForeignKey
from sqlalchemy.orm._orm_constructors import relationship
import uuid
from decimal import Decimal

from sqlalchemy import String, Numeric, Text, Boolean
from sqlalchemy.orm import Mapped, mapped_column

from app.core.database import Base
from app.models.base import TimestampMixin
from sqlalchemy.dialects.postgresql import UUID as PG_UUID

class Product(
    Base,
    TimestampMixin,
):
    __tablename__ = "products"

    id: Mapped[PG_UUID] = mapped_column(
        PG_UUID(as_uuid=True),
        primary_key=True,
        default=uuid.uuid4
    )
    name: Mapped[str] = mapped_column(
        String(255),
        nullable=False,
    )
    description: Mapped[str | None] = mapped_column(
        Text,
    )
    price: Mapped[Decimal] = mapped_column(
        Numeric(10, 2),
        nullable=False,
    )
    stock: Mapped[int] = mapped_column(
        Integer,
        nullable=False,
    )
    is_active: Mapped[bool] = mapped_column(
        Boolean,
        default=True,
        nullable=False,
    )

    category_id: Mapped[PG_UUID] = mapped_column(
        PG_UUID(as_uuid=True),
        ForeignKey("categories.id"),
        nullable=False
    )
    
    category: Mapped["Category"] = relationship(
        "Category",
        back_populates="products",
    )
