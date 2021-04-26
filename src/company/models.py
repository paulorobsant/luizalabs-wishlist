from sqlalchemy import Column, String, ForeignKey
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship

from core.database.models import DBModelMixin

"""
    Entities
"""


class Company(DBModelMixin):
    __tablename__ = "company"
    __table_args__ = {"schema": "public", "extend_existing": True}

    name = Column(String(128), nullable=False)
    email_suffix = Column(String(128), nullable=False)


class UserCompany(DBModelMixin):
    __tablename__ = "user_company"
    __table_args__ = {"schema": "public", "extend_existing": True}

    company_id = Column(UUID(as_uuid=True), ForeignKey("public.company.id"))
    company = relationship("Company", foreign_keys=[company_id])

    user_id = Column(UUID(as_uuid=True), ForeignKey("public.user.id"))
    user = relationship("User", foreign_keys=[user_id])
