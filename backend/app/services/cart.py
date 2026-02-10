from sqlalchemy.ext.asyncio import AsyncSession
from uuid import UUID
from app.repositories.cart import CartRepository
from app.repositories.product import ProductRepository
from app.models.cart_item import CartItem
from fastapi import HTTPException


class CartService:
    def __init__(self, session: AsyncSession):
        self.cart_repo = CartRepository(session)
        self.product_repo = ProductRepository(session)
        self.session = session

    async def add_to_cart(
        self, user_id: UUID, product_id: UUID, quantity: int
    ):
        if quantity <= 0:
            raise HTTPException(
                status_code=400, detail="Quantity must be greater than 0"
            )

        product = await self.product_repo.get_by_id(product_id)
        if not product or not product.is_active:
            raise HTTPException(
                status_code=404, detail="Product not available"
            )

        if product.stock < quantity:
            raise HTTPException(
                status_code=400, detail="Not enough stock"
            )

        cart = await self.cart_repo.get_active_cart(user_id)
        if not cart:
            cart = await self.cart_repo.create_cart(user_id)

        item = await self.cart_repo.get_item(cart.id, product_id)

        if item:
            new_quantity = item.quantity + quantity
            if new_quantity > product.stock:
                raise HTTPException(
                    status_code=400,
                    detail="Not enough stock",
                )
            item.quantity = new_quantity
        else:
            item = CartItem(
                cart_id=cart.id,
                product_id=product_id,
                quantity=quantity,
            )
            await self.cart_repo.add_item(item)

        await self.session.commit()
        return cart

    async def remove_from_cart(self, user_id: UUID, product_id: UUID):
        cart = await self.cart_repo.get_active_cart(user_id)
        if not cart:
            raise HTTPException(
                status_code=404, detail="Cart not found"
            )

        item = await self.cart_repo.get_item(cart.id, product_id)
        if not item:
            raise HTTPException(
                status_code=404, detail="Item not found in cart"
            )

        await self.cart_repo.remove_item(item)
        await self.session.commit()
