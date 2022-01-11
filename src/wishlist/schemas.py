from typing import Any, List
from pydantic import BaseModel


class Product(BaseModel):
    price: float
    image: str
    brand: str
    id: str
    title: str


class WishlistBase(BaseModel):
    user_id: str
    products_id: List[Product]

    class Config:
        orm_mode = True


class WishlistCreate(BaseModel):
    user_id: str
    product_id: str


class WishlistUpdate(WishlistBase):
    id: Any
    user_id: Any
    products_id: Any


class WishlistRead(WishlistBase):
    id: Any
    user_id: Any
    products_id: List[Product]
