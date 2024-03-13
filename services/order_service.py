from sqlalchemy import select, update, and_
from src.database import async_session_factory
from src.models import Fruit, Order, OrderProduct, CartProduct, Cart


class OrderService:
    @staticmethod
    async def count_order_total_price(order_id):
        async with async_session_factory() as session:
            query = select(OrderProduct).where(OrderProduct.order_id == order_id)
            order_products = await session.execute(query)

            total_price = 0

            for order_product in order_products.scalars().all():
                print(order_product.total_price)
                total_price += order_product.total_price

            query = update(Order).where(Order.id == order_id).values(total_price=total_price)
            await session.execute(query)

            await session.commit()

        return total_price

    @staticmethod
    async def remove_fruit_from_stock(fruit_id, quantity):
        async with async_session_factory() as session:
            query = select(Fruit).where(Fruit.id == fruit_id)
            res = await session.execute(query)
            fruit = res.scalar()

            fruit.total_quantity -= quantity

            await session.commit()

    @staticmethod
    async def create_order_products(data):
        async with async_session_factory() as session:
            cart_products_query = await session.execute(
                select(CartProduct)
                .join(Cart)
                .where(and_(Cart.user_id == data.user_id, Cart.is_active == True))
            )
            cart_products = cart_products_query.scalars().all()

            order_query = await session.execute(select(Order).where(Order.user_id == data.user_id))
            order = order_query.scalar()

            for cart_product in cart_products:
                new_order_product = OrderProduct(
                    order_id=order.id,
                    product_id=cart_product.product_id,
                    quantity=cart_product.quantity,
                    total_price=cart_product.total_price
                )

                session.add(new_order_product)

                await OrderService.remove_fruit_from_stock(cart_product.product_id, cart_product.quantity)

            await session.commit()
