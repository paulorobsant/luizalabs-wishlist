from sqlalchemy import Column, String, Boolean, Integer, DateTime, ForeignKey
from sqlalchemy.dialects.postgresql import ARRAY, UUID, JSONB
from sqlalchemy.orm import relationship

from core.database.models import LogModelMixin, DBModelMixin

"""
    Logs
"""


class UserLoginAttemptsLog(LogModelMixin):
    __tablename__ = "user_login_attempts_log"
    __table_args__ = {"schema": "logs", "extend_existing": True}

    email_or_username = Column(String(512), nullable=True)


"""
    Entities
"""


class User(DBModelMixin):
    __tablename__ = "user"
    __table_args__ = {"schema": "public", "extend_existing": True}

    email = Column(String(128), nullable=False)
    name = Column(String(128), nullable=True)
    phone_number = Column(String(128), nullable=True)
    surname = Column(String(128), nullable=True)
    hashed_password = Column(String(512), nullable=False)
    is_active = Column(Boolean, nullable=False, default=True)
    is_superuser = Column(Boolean, nullable=False, default=False)
    is_email_confirmed = Column(Boolean, nullable=False, default=False)
    email_confirmation_code = Column(String(512), nullable=True)
    password_reset_code = Column(String(512), nullable=True)
    access_failed_count = Column(Integer(), nullable=False, default=0)
    last_login_time = Column(DateTime, nullable=True)


class UserProfile(DBModelMixin):
    __tablename__ = "user_profile"
    __table_args__ = {"schema": "public", "extend_existing": True}

    expertises = Column(ARRAY(String))
    challenges = Column(ARRAY(String))

    total_conn_as_mentor = Column(Integer(), nullable=False, default=0)
    total_conn_as_learner = Column(Integer(), nullable=False, default=0)

    user_id = Column(UUID(as_uuid=True), ForeignKey("public.user.id"))
    user = relationship("User", foreign_keys=[user_id])

    data = Column(JSONB, nullable=True)
