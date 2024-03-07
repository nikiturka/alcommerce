from sqlalchemy import select, update, and_
from src.database import async_session_factory
from src.models import Fruit, Order, OrderProduct


class OrderService:
    @staticmethod
    async def count_order_product_total_price(product_id, quantity):
        async with async_session_factory() as session:
            query = select(Fruit).where(Fruit.id == product_id)
            fruit = await session.execute(query)

            fruit_price = fruit.scalar().price_for_kg
            total_price = fruit_price * quantity

            await session.commit()

        return total_price

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
    async def update_or_create_order_product(data):
        async with (async_session_factory() as session):
            query = select(OrderProduct).where(and_((OrderProduct.order_id == data.order_id), (OrderProduct.product_id == data.product_id)))
            res = await session.execute(query)
            existing_order_product = res.scalar()

            if existing_order_product:
                existing_order_product.quantity += data.quantity
                existing_order_product.total_price = await OrderService.count_order_product_total_price(
                    existing_order_product.product_id, existing_order_product.quantity
                )

            else:
                total_price = await OrderService.count_order_product_total_price(data.product_id, data.quantity)
                order_product = OrderProduct(
                    order_id=data.order_id,
                    product_id=data.product_id,
                    quantity=data.quantity,
                    total_price=total_price
                )
                session.add(order_product)

            await session.commit()
