from fastapi import FastAPI
from src.database import create_tables
from routers.categories import categories_router


app = FastAPI()

app.include_router(categories_router)


@app.on_event("startup")
async def startup_event():
    await create_tables()
