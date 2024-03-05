from fastapi import APIRouter, Depends
from sqlalchemy import select, insert, delete, update
from sqlalchemy.orm import selectinload

from src.database import async_session_factory
from src.models import *
from src.schema import FruitSchema

fruits_router = APIRouter(tags=["Fruits"], prefix='/fruits')


@fruits_router.get("/")
async def get_fruits():
    try:
        async with async_session_factory() as session:
            query = select(Fruit).options(selectinload(Fruit.category))
            data = await session.execute(query)
            data_converted = data.scalars().all()

        return {"fruits": data_converted}
    except Exception as e:
        return {"error": str(e)}


@fruits_router.post("/")
async def create_fruit(new_fruit: FruitSchema):
    try:
        async with async_session_factory() as session:
            query = insert(Fruit).values(**new_fruit.dict())
            await session.execute(query)
            await session.commit()

        return {"status": "200"}
    except Exception as e:
        return {"error": str(e)}


@fruits_router.get("/{fruit_id}")
async def get_fruit(fruit_id: int):
    try:
        async with async_session_factory() as session:
            query = select(Fruit).where(Fruit.id == fruit_id).options(selectinload(Fruit.category))
            data = await session.execute(query)
            data_converted = data.scalars().all()

        return {"user": data_converted}
    except Exception as e:
        return {"error": str(e)}


@fruits_router.put("/{fruit_id}")
async def update_fruit(fruit_id: int, fields_to_update: Annotated[FruitSchema, Depends()]):
    try:
        async with async_session_factory() as session:
            stmt = update(Fruit).where(Fruit.id == fruit_id).values(**fields_to_update.dict())
            await session.execute(stmt)
            await session.commit()

        return {"status": "200"}

    except Exception as e:
        return {"error": str(e)}


@fruits_router.delete("/{fruit_id}")
async def delete_fruit(fruit_id: int):
    try:
        async with async_session_factory() as session:
            query = delete(Fruit).where(Fruit.id == fruit_id)
            await session.execute(query)
            await session.commit()

        return {"status": "200"}
    except Exception as e:
        return {"error": str(e)}
