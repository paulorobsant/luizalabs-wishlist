from sqlalchemy import Column, String, Boolean, Integer, DateTime, ForeignKey
from sqlalchemy.dialects.postgresql import ARRAY, UUID, JSONB
from sqlalchemy.orm import relationship

from core.database.models import DBModelMixin

"""
    Entities
"""


class User(DBModelMixin):
    __tablename__ = "user"
    __table_args__ = {"schema": "public", "extend_existing": True}

    email = Column(String(128), nullable=False)
    name = Column(String(128), nullable=True)
    hashed_password = Column(String(512), nullable=False)

