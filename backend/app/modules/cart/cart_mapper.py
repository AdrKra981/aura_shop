from app.schemas.cart import CartItemResponse, CartResponse

def map_cart(cart) -> CartResponse:
    return CartResponse(
        id=cart.id,
        items=[
            CartItemResponse(
                product_id=item.product.id,
                product_name=item.product.name,
                product_price=item.product.price,
                quantity=item.quantity,
            )
            for item in cart.items
        ],
    )
