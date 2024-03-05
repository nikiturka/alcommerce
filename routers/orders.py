from fastapi import APIRouter, Depends
from sqlalchemy import select, insert, delete, update
from sqlalchemy.orm import selectinload

from src.database import async_session_factory
from src.models import *
from src.schema import OrderSchema

orders_router = APIRouter(tags=["Orders"], prefix='/orders')


@orders_router.get("/")
async def get_orders():
    try:
        async with async_session_factory() as session:
            query = select(Order).options(selectinload(Order.user))
            data = await session.execute(query)
            data_converted = data.scalars().all()

        return {"orders": data_converted}
    except Exception as e:
        return {"error": str(e)}


@orders_router.post("/")
async def create_order(new_order: OrderSchema):
    try:
        async with async_session_factory() as session:
            query = insert(Order).values(**new_order.dict())
            await session.execute(query)
            await session.commit()

        return {"status": "200"}
    except Exception as e:
        return {"error": str(e)}


@orders_router.get("/{order_id}")
async def get_order(order_id: int):
    try:
        async with async_session_factory() as session:
            query = select(Order).where(Order.id == order_id).options(selectinload(Order.user))
            data = await session.execute(query)
            data_converted = data.scalars().all()

        return {"order": data_converted}
    except Exception as e:
        return {"error": str(e)}


@orders_router.put("/{order_id}")
async def update_order(order_id: int, fields_to_update: Annotated[OrderSchema, Depends()]):
    try:
        async with async_session_factory() as session:
            stmt = update(Order).where(Order.id == order_id).values(**fields_to_update.dict())
            await session.execute(stmt)
            await session.commit()

        return {"status": "200"}

    except Exception as e:
        return {"error": str(e)}


@orders_router.delete("/{order_id}")
async def delete_order(order_id: int):
    try:
        async with async_session_factory() as session:
            query = delete(Order).where(Order.id == order_id)
            await session.execute(query)
            await session.commit()

        return {"status": "200"}
    except Exception as e:
        return {"error": str(e)}
