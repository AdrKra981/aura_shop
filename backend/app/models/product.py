from sqlalchemy.orm._orm_constructors import relationship
import uuid
from decimal import Decimal

from sqlalchemy import String, Numeric, Text, Boolean
from sqlalchemy.orm import Mapped, mapped_column

from app.core.database import Base
from app.models.base import UUIDPrimaryKeyMixin, TimestampMixin


class Product(
    Base,
    UUIDPrimaryKeyMixin,
    TimestampMixin,
):
    __tablename__ = "products"

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
    is_active: Mapped[bool] = mapped_column(
        Boolean,
        default=True,
        nullable=False,
    )

    category_id: Mapped[str] = mapped_column(
        String(36),
        nullable=False,
    )
    category: Mapped["Category"] = relationship(
        "Category",
        back_populates="products",
    )
