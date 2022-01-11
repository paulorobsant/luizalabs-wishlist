from typing import Any, List
from pydantic import BaseModel


class UserBase(BaseModel):
    name: str = None
    email: str = None

    class Config:
        orm_mode = True


class User(UserBase):
    id: int


class UserCreate(UserBase):
    name: str
    email: str


class UserRead(UserBase):
    id: Any
    name: str
    email: str


class UserUpdate(UserBase):
    id: Any
