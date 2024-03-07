from fastapi import APIRouter, Depends
from sqlalchemy import select, delete, update

from services.order_service import OrderService
from src.database import async_session_factory
from src.models import *
from src.schema import OrderProductSchema

order_products_router = APIRouter(tags=["Order products"], prefix='/order_products')


@order_products_router.get("/")
async def get_order_products():
    try:
        async with async_session_factory() as session:
            query = select(OrderProduct)
            data = await session.execute(query)
            data_converted = data.scalars().all()

        return {"order_products": data_converted}
    except Exception as e:
        return {"error": str(e)}


@order_products_router.post("/")
async def create_order_product(data: Annotated[OrderProductSchema, Depends()]):
    try:
        await OrderService.update_or_create_order_product(data)
        await OrderService.count_order_total_price(data.order_id)
        await OrderService.remove_fruit_from_stock(data.product_id, data.quantity)
        return {"status": "200"}
    except Exception as e:
        return {"error": str(e)}


@order_products_router.get("/{order_product_id}")
async def get_order_product(order_product_id: int):
    try:
        async with async_session_factory() as session:
            query = select(OrderProduct).where(OrderProduct.id == order_product_id)
            data = await session.execute(query)
            data_converted = data.scalars().all()

        return {"order_product": data_converted}
    except Exception as e:
        return {"error": str(e)}


@order_products_router.put("/{order_product_id}")
async def update_order_product(order_product_id: int, fields_to_update: Annotated[OrderProductSchema, Depends()]):
    try:
        async with async_session_factory() as session:
            stmt = update(OrderProduct).where(OrderProduct.id == order_product_id).values(**fields_to_update.dict())
            await session.execute(stmt)
            await session.commit()

        return {"status": "200"}

    except Exception as e:
        return {"error": str(e)}


@order_products_router.delete("/{order_product_id}")
async def delete_order_product(order_product_id: int):
    try:
        async with async_session_factory() as session:
            query = delete(OrderProduct).where(OrderProduct.id == order_product_id)
            await session.execute(query)
            await session.commit()

        return {"status": "200"}
    except Exception as e:
        return {"error": str(e)}
