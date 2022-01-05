from typing import Any, List
from pydantic import BaseModel


class UserBase(BaseModel):
    name: str = None
    email: str = None
    password: str = None

    class Config:
        orm_mode = True


class User(UserBase):
    id: int
    is_active: bool


class UserCreate(UserBase):
    name: str
    email: str
    password: str


class UserRead(UserBase):
    id: Any
    name: str
    email: str


class UserUpdate(UserBase):
    id: Any
