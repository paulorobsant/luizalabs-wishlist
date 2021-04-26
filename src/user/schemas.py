from typing import Any, List

from pydantic import BaseModel


class UserBase(BaseModel):
    name: str = None
    email: str = None
    username: str = None

    class Config:
        orm_mode = True


class User(UserBase):
    id: int
    is_active: bool


class UserCreate(UserBase):
    name: str
    email: str
    username: str
    password: str


class UserRead(UserBase):
    id: Any
    name: str
    email: str


# User Profile

class UserProfileCreate(UserBase):
    expertises: List[str]
    challenges: List[str]


class UserProfileRead(UserBase):
    expertises: Any
    challenges: List[str] = None
