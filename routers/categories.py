from fastapi import APIRouter
from sqlalchemy import select, insert, delete, update
from sqlalchemy.exc import SQLAlchemyError

from src.database import async_session_factory
from src.models import *
from src.schema import CategorySchema

fruits_router = APIRouter(tags=["Categories"], prefix='/categories')


@fruits_router.get("/")
async def get_categories():
    try:
        async with async_session_factory() as session:
            query = select(Category)
            data = await session.execute(query)
            data_converted = data.scalars().all()

        return {"categories": data_converted}
    except Exception as e:
        return {"error": str(e)}


@fruits_router.post("/")
async def create_category(new_category: CategorySchema):
    try:
        async with async_session_factory() as session:
            query = insert(Category).values(**new_category.dict())
            await session.execute(query)
            await session.commit()

        return {"status": "200"}
    except Exception as e:
        return {"error": str(e)}


@fruits_router.get("/{category_id}")
async def get_category(category_id: int):
    try:
        async with async_session_factory() as session:
            query = select(Category).where(Category.id == category_id)
            data = await session.execute(query)
            data_converted = data.scalars().all()

        return {"category": data_converted}
    except Exception as e:
        return {"error": str(e)}


@fruits_router.put("/{category_id}")
async def update_category(category_id: int, fields_to_update: CategorySchema):
    try:
        async with async_session_factory() as session:
            stmt = update(Category).where(Category.id == category_id).values(**fields_to_update.dict())
            await session.execute(stmt)
            await session.commit()

        return {"status": "200"}
    except Exception as e:
        return {"error": str(e)}


@fruits_router.delete("/{category_id}")
async def delete_category(category_id: int):
    try:
        async with async_session_factory() as session:
            query = delete(Category).where(Category.id == category_id)
            await session.execute(query)
            await session.commit()

        return {"status": "200"}
    except Exception as e:
        return {"error": str(e)}
