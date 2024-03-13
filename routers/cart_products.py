from fastapi import APIRouter, Depends
from sqlalchemy import select, delete, update
from services.cart_products_service import CartProductsService
from src.database import async_session_factory
from src.models import *
from src.schema import CartProductSchema

cart_products_router = APIRouter(tags=["Cart Products"], prefix='/cart_products')


@cart_products_router.get("/")
async def get_cart_products():
    try:
        async with async_session_factory() as session:
            query = select(CartProduct)
            data = await session.execute(query)
            data_converted = data.scalars().all()

        return {"cart_products": data_converted}
    except Exception as e:
        return {"error": str(e)}


@cart_products_router.post("/")
async def create_cart_product(data: CartProductSchema):
    try:
        await CartProductsService.check_product_in_stock(data.quantity, data.product_id)
        await CartProductsService.count_cart_product_total_price(data.product_id, data.quantity)
        await CartProductsService.update_or_create_cart_product(data)
        return {"status": "200"}
    except Exception as e:
        return {"error": str(e)}


@cart_products_router.get("/{cart_product_id}")
async def get_cart_product(cart_product_id: int):
    try:
        async with async_session_factory() as session:
            query = select(CartProduct).where(CartProduct.id == cart_product_id)
            data = await session.execute(query)
            data_converted = data.scalars().all()

        return {"cart_product": data_converted}
    except Exception as e:
        return {"error": str(e)}


@cart_products_router.put("/{cart_product_id}")
async def update_cart_product(cart_product_id: int, fields_to_update: Annotated[CartProductSchema, Depends()]):
    try:
        async with async_session_factory() as session:
            stmt = update(CartProduct).where(CartProduct.id == cart_product_id).values(**fields_to_update.dict())
            await session.execute(stmt)
            await session.commit()

        return {"status": "200"}

    except Exception as e:
        return {"error": str(e)}


@cart_products_router.delete("/{cart_product_id}")
async def delete_order(cart_product_id: int):
    try:
        async with async_session_factory() as session:
            query = delete(CartProduct).where(CartProduct.id == cart_product_id)
            await session.execute(query)
            await session.commit()

        return {"status": "200"}
    except Exception as e:
        return {"error": str(e)}
