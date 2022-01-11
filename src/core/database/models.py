import sqlalchemy
from bson import ObjectId
from sqlalchemy import Column, DateTime, func, Boolean
from sqlalchemy import String, ForeignKey
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.ext.declarative import declared_attr

from core.database.session import Base
from core.serializers import DBSerializerMixin


class DBModelMixin(Base, DBSerializerMixin):
    __abstract__ = True

    id = Column(UUID(as_uuid=True), primary_key=True, server_default=sqlalchemy.text("uuid_generate_v4()"))
    created_at = Column(DateTime, default=func.now())
    updated_at = Column(DateTime, default=func.now(), onupdate=func.now())
    is_deleted = Column(Boolean, nullable=False, default=False)


# class LogModelMixin(Base, DBSerializerMixin):
#     __abstract__ = True
#
#     id = Column(UUID(as_uuid=True), primary_key=True, server_default=sqlalchemy.text("uuid_generate_v4()"))
#     browser_info = Column(String(512), nullable=True)
#     client_ip_address = Column(String(18), nullable=False)
#     client_name = Column(String(512), nullable=True)
#     created_at = Column(DateTime, default=func.now())
#     updated_at = Column(DateTime, default=func.now(), onupdate=func.now())
#     description = Column(String(1024), nullable=True)
