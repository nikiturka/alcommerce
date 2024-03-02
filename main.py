from fastapi import FastAPI
from src.database import create_tables
from routers.categories import fruits_router


app = FastAPI()

app.include_router(fruits_router)


@app.on_event("startup")
async def startup_event():
    await create_tables()
