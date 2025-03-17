from pydantic import BaseModel
from typing import Optional


class User(BaseModel):
    id: int
    name: str
    lastName: Optional[str] = None
    age: int


class MessageResponse(BaseModel):
    message: str


class Product(BaseModel):
    id: int
    name: str
    price: int


class UserBasic(BaseModel):
    username: str
    email: str
    disabled: bool


class UserDbBasic(UserBasic):
    password: str


class responseToken(BaseModel):
    access_token: str
    token_type: str
