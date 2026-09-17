from pydantic import BaseModel , ConfigDict
from typing import Optional

class Product(BaseModel):
    id: int
    name: str
    price: float
    model_config = ConfigDict(from_attributes=True)


class ProductCreate(BaseModel):
    name: str
    price: float
    owner_id: int

class ProductUpdate(BaseModel):
    name: Optional[str] = None
    price: Optional[float] = None


class UserCreate(BaseModel):
    name: str
    password: str


class User(BaseModel):
    id: int
    name: str

    model_config = ConfigDict(from_attributes=True)

class UserWithProducts(User):
    products: list[Product]

class LoginRequest(BaseModel):
    name: str
    password: str