from typing import Any
from pydantic import BaseModel


class CompanyBase(BaseModel):
    name: str = None
    email_suffix: str = None

    class Config:
        orm_mode = True


class CompanyCreate(CompanyBase):
    name: str
    email_suffix: str


class CompanyRead(CompanyBase):
    id: Any
    name: str
    email_suffix: str
