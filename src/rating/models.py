import enum

from sqlalchemy import Column, String, ForeignKey
from sqlalchemy.dialects.postgresql import ENUM, UUID
from sqlalchemy.orm import relationship

from core.database.models import DBModelMixin

"""
    Enums
"""


class RatingQuestionType(enum.Enum):
    TEXT = 1
    NUMBER = 2


"""
    Entities
"""


class RatingForm(DBModelMixin):
    __tablename__ = "rating_form"
    __table_args__ = {"schema": "public", "extend_existing": True}

    title = Column(String(128), nullable=False, unique=True, index=True)


class RatingQuestion(DBModelMixin):
    __tablename__ = "rating_question"
    __table_args__ = {"schema": "public", "extend_existing": True}

    type = Column(ENUM(RatingQuestionType), nullable=False)
    question = Column(String(256), nullable=True)


class RatingFormQuestion(DBModelMixin):
    __tablename__ = "rating_forms_questions"
    __table_args__ = {"schema": "public", "extend_existing": True}

    rating_question_id = Column(UUID(as_uuid=True), ForeignKey("public.rating_question.id"))
    rating_question = relationship("RatingQuestion", foreign_keys=[rating_question_id])

    rating_form_id = Column(UUID(as_uuid=True), ForeignKey("public.rating_form.id"))
    rating_form = relationship("Rating", foreign_keys=[rating_form_id])
