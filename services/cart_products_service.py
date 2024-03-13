from sqlalchemy import select, and_

from src.database import async_session_factory
from src.models import Fruit, CartProduct


class CartProductsService:
    @staticmethod
    async def check_product_in_stock(quantity, product_id):
        async with async_session_factory() as session:
            fruit = await session.execute(select(Fruit).where(Fruit.id == product_id))

            if quantity > fruit.scalar().total_quantity:
                raise Exception("Error: Out of stock")

        return
    
    @staticmethod
    async def count_cart_product_total_price(product_id, quantity):
        async with async_session_factory() as session:
            query = select(Fruit).where(Fruit.id == product_id)
            fruit = await session.execute(query)

            fruit_price = fruit.scalar().price_for_kg
            total_price = fruit_price * quantity

            await session.commit()

        return total_price

    @staticmethod
    async def update_or_create_cart_product(data):
        async with (async_session_factory() as session):
            query = select(CartProduct).where(and_((CartProduct.cart_id == data.cart_id), (CartProduct.product_id == data.product_id)))
            res = await session.execute(query)
            existing_order_product = res.scalar()

            if existing_order_product:
                existing_order_product.quantity += data.quantity
                existing_order_product.total_price = await CartProductsService.count_cart_product_total_price(
                    existing_order_product.product_id, existing_order_product.quantity
                )

            else:
                total_price = await CartProductsService.count_cart_product_total_price(data.product_id, data.quantity)
                cart_product = CartProduct(
                    cart_id=data.cart_id,
                    product_id=data.product_id,
                    quantity=data.quantity,
                    total_price=total_price
                )
                session.add(cart_product)

            await session.commit()