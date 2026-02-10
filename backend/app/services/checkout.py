import json
from sqlalchemy.ext.asyncio import AsyncSession
from fastapi import HTTPException
from uuid import UUID
from decimal import Decimal

from app.repositories.cart import CartRepository
from app.repositories.order import OrderRepository
from app.repositories.product import ProductRepository
from app.models.order import Order, OrderStatus
from app.models.order_item import OrderItem
from app.payments.fake import FakePaymentProvider
from app.repositories.idempotency import IdempotencyRepository


class CheckoutService:
    def __init__(self, session: AsyncSession):
        self.session = session
        self.cart_repo = CartRepository(session)
        self.order_repo = OrderRepository(session)
        self.product_repo = ProductRepository(session)
        self.payment_provider = FakePaymentProvider()
        self.idempotency_repo = IdempotencyRepository(session)

    async def checkout(self, user_id: UUID, idempotency_key: str | None = None) -> Order:
        if idempotency_key:
            existing = await self.idempotency_repo.get(idempotency_key)
            if existing:
                return json.loads(existing.response_body)

        async with self.session.begin():

            cart = await self.cart_repo.get_active_cart(user_id)
            if not cart or not cart.items:
                raise HTTPException(
                    status_code=400,
                    detail="Cart is empty",
                )

            total_price = Decimal("0.00")
            locked_products = {}
            order_items: list[OrderItem] = []

            for item in cart.items:
                product = await self.product_repo.get_for_update(item.product_id)

                if not product or not product.is_active:
                    raise HTTPException(
                        status_code=400,
                        detail=f"Product {product.name} is inactive",
                    )

                if product.stock < item.quantity:
                    raise HTTPException(
                        status_code=400,
                        detail=f"Not enough stock for {product.name}",
                    )

                locked_products[product.id] = product
                total_price += product.price * item.quantity

            # PAYMENT (external side-effect)
            payment = await self.payment_provider.charge(
                user_id=user_id,
                amount=total_price,
            )

            if not payment.success:
                raise HTTPException(
                    status_code=400,
                    detail="Payment failed",
                )

            # CREATE ORDER
            order = Order(
                user_id=user_id,
                status=OrderStatus.PAID,
                total_price=total_price,
            )
            await self.order_repo.create_order(order)

            # ORDER ITEMS + STOCK UPDATE
            for item in cart.items:
                product = item.product
                product.stock -= item.quantity

                order_item = OrderItem(
                    order_id=order.id,
                    product_name=product.name,
                    product_price=product.price,
                    quantity=item.quantity,
                )
                order_items.append(order_item)

            await self.order_repo.add_order_items(order_items)

            # CLOSE CART
            cart.is_active = False

            response = {
                "order_id": str(order.id),
                "total_price": str(order.total_price),
                "status": order.status,
            }

            await self.idempotency_repo.save(
                key=idempotency_key,
                response_body=json.dumps(response),
            )

            return response
