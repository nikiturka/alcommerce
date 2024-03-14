from fastapi import APIRouter, Depends
from sqlalchemy import select, insert, delete, update
from sqlalchemy.orm import selectinload

from src.database import async_session_factory
from src.models import *
from src.schema import ReviewSchema

reviews_router = APIRouter(tags=["Reviews"], prefix='/reviews')


@reviews_router.get("/")
async def get_reviews():
    try:
        async with async_session_factory() as session:
            query = select(Review)
            data = await session.execute(query)
            data_converted = data.scalars().all()

        return {"reviews": data_converted}
    except Exception as e:
        return {"error": str(e)}


@reviews_router.post("/")
async def create_review(new_review: ReviewSchema):
    try:
        async with async_session_factory() as session:
            query = insert(Review).values(**new_review.dict())
            await session.execute(query)
            await session.commit()

        return {"status": "200"}
    except Exception as e:
        return {"error": str(e)}


@reviews_router.get("/{review_id}")
async def get_review(review_id: int):
    try:
        async with async_session_factory() as session:
            query = select(Review).where(Review.id == review_id)
            data = await session.execute(query)
            data_converted = data.scalars().all()

        return {"review": data_converted}
    except Exception as e:
        return {"error": str(e)}


@reviews_router.put("/{review_id}")
async def update_review(review_id: int, fields_to_update: Annotated[ReviewSchema, Depends()]):
    try:
        async with async_session_factory() as session:
            stmt = update(Review).where(Review.id == review_id).values(**fields_to_update.dict())
            await session.execute(stmt)
            await session.commit()

        return {"status": "200"}

    except Exception as e:
        return {"error": str(e)}


@reviews_router.delete("/{review_id}")
async def delete_review(review_id: int):
    try:
        async with async_session_factory() as session:
            query = delete(Review).where(Review.id == review_id)
            await session.execute(query)
            await session.commit()

        return {"status": "200"}
    except Exception as e:
        return {"error": str(e)}
