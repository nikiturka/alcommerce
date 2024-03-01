from fastapi import FastAPI
from src.database import create_tables


app = FastAPI()


@app.get("/")
async def root():
    return {"message": "Hello World"}


create_tables()
