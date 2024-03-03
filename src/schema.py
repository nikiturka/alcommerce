from pydantic import BaseModel


class CategorySchema(BaseModel):
    name: str


class UserSchema(BaseModel):
    name: str
    surname: str


class UserOptionalSchema(UserSchema):
    name: str | None = None
    surname: str | None = None
