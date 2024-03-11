from fastapi import APIRouter, Depends
from sqlalchemy import select, insert, delete, update
from sqlalchemy.orm import selectinload

from src.database import async_session_factory
from src.models import *
from src.schema import OrderSchema, CartSchema

carts_router = APIRouter(tags=["Carts"], prefix='/carts')


@carts_router.get("/")
async def get_carts():
    try:
        async with async_session_factory() as session:
            query = select(Cart)
            data = await session.execute(query)
            data_converted = data.scalars().all()

        return {"carts": data_converted}
    except Exception as e:
        return {"error": str(e)}


@carts_router.post("/")
async def create_cart(new_cart: CartSchema):
    try:
        async with async_session_factory() as session:
            query = insert(Cart).values(**new_cart.dict())
            await session.execute(query)
            await session.commit()

        return {"status": "200"}
    except Exception as e:
        return {"error": str(e)}


@carts_router.get("/{cart_id}")
async def get_cart(cart_id: int):
    try:
        async with async_session_factory() as session:
            query = select(Cart).where(Cart.id == cart_id)
            data = await session.execute(query)
            data_converted = data.scalars().all()

        return {"cart": data_converted}
    except Exception as e:
        return {"error": str(e)}


@carts_router.put("/{cart_id}")
async def update_cart(cart_id: int, fields_to_update: Annotated[CartSchema, Depends()]):
    try:
        async with async_session_factory() as session:
            stmt = update(Cart).where(Cart.id == cart_id).values(**fields_to_update.dict())
            await session.execute(stmt)
            await session.commit()

        return {"status": "200"}

    except Exception as e:
        return {"error": str(e)}


@carts_router.delete("/{cart_id}")
async def delete_order(cart_id: int):
    try:
        async with async_session_factory() as session:
            query = delete(Cart).where(Cart.id == cart_id)
            await session.execute(query)
            await session.commit()

        return {"status": "200"}
    except Exception as e:
        return {"error": str(e)}
