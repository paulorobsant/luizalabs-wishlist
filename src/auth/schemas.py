from typing import Optional, Any
from pydantic import BaseModel, EmailStr


class Token(BaseModel):
    access_token: str
    token_type: Any
    expires_in: int = None
    user_id: int = None


class TokenPayload(BaseModel):
    sub: Optional[str] = None


class AuthenticatedUser(BaseModel):
    email: EmailStr = None
    is_active: bool = None
    is_superuser: bool = None
    username: str = None
    name: str = None

    class Config:
        orm_mode = True


class AuthenticatedUserUpdate(BaseModel):
    email: EmailStr = None
    username: str = None
    name: str = None

    class Config:
        orm_mode = True


class UserRegister(BaseModel):
    email: EmailStr
    username: str
    name: str
    password: str
    code: str = ""


class AuthLinkedin(BaseModel):
    code: str
