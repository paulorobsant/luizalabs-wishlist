import uuid
from sqlalchemy_serializer import SerializerMixin


class DBSerializerMixin(SerializerMixin):
    serialize_types = (
        (uuid.UUID, lambda x: str(x)),
    )
