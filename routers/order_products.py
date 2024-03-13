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
