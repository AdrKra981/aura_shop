from app.models import CartItem
from sqlalchemy.orm import selectinload
from app.models.cart import Cart
from sqlalchemy.ext.asyncio import AsyncSession
import uuid

class CartRepository:
    def __init__(self, session: AsyncSession):
        self.session = session

    async def get_active_cart(self, user_id: uuid.UUID):
        result = await self.session.execute(select(Cart).where(Cart.user_id == user_id, Cart.is_active == True).options(selectinload(Cart.items).selectinload(CartItem.product)))
        return result.scalar_one_or_none()

    async def create_cart(self, user_id: uuid.UUID):
        cart = Cart(user_id=user_id)
        self.session.add(cart)
        await self.session.flush()
        return cart

    async def get_item(self, cart_id: uuid.UUID, product_id: uuid.UUID) -> CartItem | None:
        result = await self.session.execute(select(CartItem).where(CartItem.cart_id == cart_id, CartItem.product_id == product_id))
        return result.scalar_one_or_none()

    async def add_item(self, item: CartItem) -> None:
        self.session.add(item)

    async def remove_item(self, item: CartItem) -> None:
        await self.session.delete(item)
