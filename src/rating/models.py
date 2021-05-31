import enum

from sqlalchemy import Column, String, ForeignKey, DECIMAL
from sqlalchemy.dialects.postgresql import UUID, ENUM
from sqlalchemy.orm import relationship

from core.database.models import DBModelMixin

# """
#     Enums
# """
#
#
# class RatingCriteriaType(enum.Enum):
#     TEXT = 1
#     POINTS = 2
#
#
# """
#     Entities
# """
#
#
# class Rating(DBModelMixin):
#     __tablename__ = "rating"
#     __table_args__ = {"schema": "public", "extend_existing": True}
#
#
# class RatingCriteria(DBModelMixin):
#     __tablename__ = "rating_criteria"
#     __table_args__ = {"schema": "public", "extend_existing": True}
#
#     type = Column(ENUM(RatingCriteriaType), nullable=False)
#     question = Column(DECIMAL(), nullable=True)
#     answer = Column(String(), nullable=False)
#
#     user_id = Column(UUID(as_uuid=True), ForeignKey("public.user.id"))
#     user = relationship("User", foreign_keys=[user_id])
