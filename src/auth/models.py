import enum

from sqlalchemy import Column, Boolean, Integer, ForeignKey, String
from sqlalchemy.dialects.postgresql import ENUM, UUID

from core.database.models import LogModelMixin, DBModelMixin

"""
    Logs
"""


class AuthLoginAttemptsLog(LogModelMixin):
    __tablename__ = "auth_login_attempts_log"
    __table_args__ = {"schema": "logs", "extend_existing": True}

    email_or_username = Column(String(512), nullable=True)


"""
    Entities
"""


class TokenType(enum.Enum):
    jwt = 1
    social = 2


class Token(DBModelMixin):
    __tablename__ = "token"
    __table_args__ = {"schema": "public", "extend_existing": True}

    is_revoked = Column(Boolean, nullable=False, default=False)
    user_id = Column(UUID(), ForeignKey("public.user.id"))
    token_type = Column(ENUM(TokenType))
    expires_in = Column(Integer)
    access_token = Column(String(1024), nullable=False)
