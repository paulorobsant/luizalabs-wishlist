from sqlalchemy import Column, String, Boolean, Integer, DateTime, ForeignKey
from sqlalchemy.dialects.postgresql import ARRAY, UUID, JSONB
from sqlalchemy.orm import relationship

from core.database.models import DBModelMixin

"""
    Entities
"""


class Wishlist(DBModelMixin):
    __tablename__ = "wishlist"
    __table_args__ = {"schema": "public", "extend_existing": True}

    products_id = Column(ARRAY(String), nullable=False)

    user_id = Column(UUID(as_uuid=True), ForeignKey("public.user.id"))
    user = relationship("User", foreign_keys=[user_id])
