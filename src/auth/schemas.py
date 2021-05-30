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
    username: str
    name: str
    password: str
    code: str = ""


class UserResetPassword(BaseModel):
    password: str
    code: str = ""


class UserForgotPassword(BaseModel):
    email: str


class UserInvitation(BaseModel):
    email: str
    company_id: str


class UserAuthenticated(BaseModel):
    email: EmailStr = None
    is_active: bool = None
    is_superuser: bool = None
    name: str
