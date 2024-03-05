from fastapi import FastAPI
from src.database import create_tables
from routers.categories import categories_router
from routers.users import users_router
from routers.fruits import fruits_router
from routers.orders import orders_router


app = FastAPI()

app.include_router(categories_router)
app.include_router(users_router)
app.include_router(fruits_router)
app.include_router(orders_router)


@app.on_event("startup")
async def startup_event():
    await create_tables()
