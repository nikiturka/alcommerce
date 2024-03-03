from fastapi import FastAPI
from src.database import create_tables
from routers.categories import categories_router
from routers.users import users_router


app = FastAPI()

app.include_router(categories_router)
app.include_router(users_router)

@app.on_event("startup")
async def startup_event():
    await create_tables()
