import enum

from sqlalchemy import Column, Integer, ForeignKey, DateTime, String, Boolean
from sqlalchemy.dialects.postgresql import ENUM, JSONB, INTEGER, UUID
from sqlalchemy.orm import relationship
from core.database.models import DBModelMixin

"""
    Enums
"""


class MatchRequestStatus(enum.Enum):
    PENDING = 1
    FINISHED = 2
    CANCELLED = 3
    OVERFLOWED = 4


class MatchStatus(enum.Enum):
    PENDING = 1
    FINISHED = 2
    CANCELLED = 3
    IN_PROGRESS = 4


class MatchStep(enum.Enum):
    AWAITING_FOR_MENTOR_ACCEPTANCE = 1
    AWAITING_FOR_LEARNER_ACCEPTANCE = 2
    MENTOR_SUGGEST_SCHEDULING = 3
    LEARNER_SUGGEST_SCHEDULING = 4
    MENTOR_CONFIRM_SCHEDULING = 5
    LEARNER_CONFIRM_SCHEDULING = 6
    SCHEDULING_CONFIRMED = 7
    IN_PROGRESS = 8


"""
    Entities
"""


class MatchRequest(DBModelMixin):
    __tablename__ = "match_request"
    __table_args__ = {"schema": "public", "extend_existing": True}

    status = Column(ENUM(MatchRequestStatus), nullable=False)
    data = Column(JSONB, nullable=False)
    priority = Column(INTEGER, nullable=False, default=0)

    user_id = Column(UUID(as_uuid=True), ForeignKey("public.user.id"))
    user = relationship("User", foreign_keys=[user_id])


class Match(DBModelMixin):
    __tablename__ = "match"
    __table_args__ = {"schema": "public", "extend_existing": True}

    start_datetime = Column(DateTime, nullable=False)
    end_datetime = Column(DateTime, nullable=False)

    latest_alert = Column(DateTime, nullable=True)

    status = Column(ENUM(MatchStatus), nullable=False)
    current_step = Column(ENUM(MatchStep), nullable=False)

    mentor_id = Column(UUID(as_uuid=True), ForeignKey("public.user.id"))
    mentor = relationship("User", foreign_keys=[mentor_id])

    learner_id = Column(UUID(as_uuid=True), ForeignKey("public.user.id"))
    learner = relationship("User", foreign_keys=[learner_id])

    is_approved = Column(Boolean, nullable=False, default=False)
    data = Column(JSONB, nullable=False)


class MatchTerm(DBModelMixin):
    __tablename__ = "match_term"
    __table_args__ = {"schema": "public", "extend_existing": True}

    label = Column(String(128), nullable=False, unique=True, index=True)
    value = Column(Integer(), unique=True)

    is_approved = Column(Boolean, nullable=False, default=False)


class MatchTraining(DBModelMixin):
    __tablename__ = "match_training"
    __table_args__ = {"schema": "public", "extend_existing": True}

    total_prev_entries = Column(Integer(), nullable=False)
    total_new_entries = Column(Integer(), nullable=False)


class MatchReview(DBModelMixin):
    __tablename__ = "match_review"
    __table_args__ = {"schema": "public", "extend_existing": True}

    comment = Column(String(256), nullable=False, unique=True, index=True)

    user_id = Column(UUID(as_uuid=True), ForeignKey("public.user.id"))
    user = relationship("User", foreign_keys=[user_id])

    match_id = Column(UUID(as_uuid=True), ForeignKey("public.match.id"))
    match = relationship("Match", foreign_keys=[match_id])


# class MatchRatingAnswer(DBModelMixin):
#     __tablename__ = "match_rating_answer"
#     __table_args__ = {"schema": "public", "extend_existing": True}
#
#     answer = Column(String(512), nullable=False)
#
#     user_id = Column(UUID(as_uuid=True), ForeignKey("public.user.id"))
#     user = relationship("User", foreign_keys=[user_id])
#
#     rating_question_id = Column(UUID(as_uuid=True), ForeignKey("public.rating_question.id"))
#     rating_question = relationship("RatingQuestion", foreign_keys=[rating_question_id], back_populates="answers")
#
#     match_id = Column(UUID(as_uuid=True), ForeignKey("public.match.id"), index=True)
#     match = relationship("Match", foreign_keys=[match_id])
