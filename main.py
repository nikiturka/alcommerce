from fastapi import FastAPI
from src.database import create_tables
from routers.categories import categories_router
from routers.users import users_router
from routers.fruits import fruits_router
from routers.orders import orders_router
from routers.order_products import order_products_router
from routers.carts import carts_router
from routers.cart_products import cart_products_router


app = FastAPI()

app.include_router(categories_router)
app.include_router(users_router)
app.include_router(fruits_router)
app.include_router(orders_router)
app.include_router(order_products_router)
app.include_router(carts_router)
app.include_router(cart_products_router)


@app.on_event("startup")
async def startup_event():
    await create_tables()
