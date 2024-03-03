from typing import Optional

from fastapi import APIRouter, Depends
from sqlalchemy import select, insert, delete, update
from src.database import async_session_factory
from src.models import *
from src.schema import UserSchema, UserOptionalSchema

users_router = APIRouter(tags=["Users"], prefix='/users')


@users_router.get("/")
async def get_users():
    try:
        async with async_session_factory() as session:
            query = select(User)
            data = await session.execute(query)
            data_converted = data.scalars().all()

        return {"users": data_converted}
    except Exception as e:
        return {"error": str(e)}


@users_router.post("/")
async def create_user(new_user: Annotated[UserSchema, Depends()]):
    try:
        async with async_session_factory() as session:
            query = insert(User).values(**new_user.dict())
            await session.execute(query)
            await session.commit()

        return {"status": "200"}
    except Exception as e:
        return {"error": str(e)}


@users_router.get("/{user_id}")
async def get_user(user_id: int):
    try:
        async with async_session_factory() as session:
            query = select(User).where(User.id == user_id)
            data = await session.execute(query)
            data_converted = data.scalars().all()

        return {"user": data_converted}
    except Exception as e:
        return {"error": str(e)}


@users_router.put("/{user_id}")
async def update_user(user_id: int, fields_to_update: Annotated[UserSchema, Depends()]):
    try:
        async with async_session_factory() as session:
            stmt = update(User).where(User.id == user_id).values(**fields_to_update.dict())
            await session.execute(stmt)
            await session.commit()

        return {"status": "200"}

    except Exception as e:
        return {"error": str(e)}


@users_router.patch("/{user_id}")
async def partially_update_user(user_id: int, fields_to_update: Annotated[UserOptionalSchema, Depends()]):
    try:
        async with async_session_factory() as session:
            stmt = update(User).where(User.id == user_id).values(**fields_to_update.dict(exclude_unset=True))
            await session.execute(stmt)
            await session.commit()

        return {"status": "200"}

    except Exception as e:
        return {"error": str(e)}


@users_router.delete("/{user_id}")
async def delete_user(user_id: int):
    try:
        async with async_session_factory() as session:
            query = delete(User).where(User.id == user_id)
            await session.execute(query)
            await session.commit()

        return {"status": "200"}
    except Exception as e:
        return {"error": str(e)}
