from typing import Optional, Any
from pydantic import BaseModel, EmailStr


class Token(BaseModel):
    access_token: str
    token_type: Any
    expires_in: int = None
    user_id: int = None


class TokenPayload(BaseModel):
    sub: Optional[str] = None


class UserLogin(BaseModel):
    email: EmailStr
    password: str


class UserRegister(BaseModel):
    email: EmailStr
    name: str
    password: str


class UserResetPassword(BaseModel):
    password: str
    code: str = ""


class UserForgotPassword(BaseModel):
    email: str

