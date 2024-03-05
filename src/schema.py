from pydantic import BaseModel


class CategorySchema(BaseModel):
    name: str


class UserSchema(BaseModel):
    name: str
    surname: str


class FruitSchema(BaseModel):
    name: str
    description: str
    price_for_kg: float
    total_quantity: int
    rating: float = None
    category_id: int

