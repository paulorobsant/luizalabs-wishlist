import datetime
import json
import user.services as user_services

from core.database.session import Session
from core.security import get_password_hash
from core.security import verify_password
from auth import schemas
from auth.models import Token
from user.models import User


def authenticate(db: Session, email: str, password: str):
    db_user = db.query(User).filter(User.email == email).first()

    if not db_user:
        return None

    if not verify_password(password, db_user.hashed_password):
        return None

    return db_user


def register(db: Session, entry: schemas.UserRegister):
    db_obj = User(
        email=entry.email,
        hashed_password=get_password_hash(entry.password),
        name=entry.name,
    )

    db.add(db_obj)
    db.commit()
    db.refresh(db_obj)

    return db_obj


def save_token(db: Session, *, obj_in: schemas.Token):
    db_obj = Token(
        access_token=obj_in.access_token,
        token_type=obj_in.token_type,
        expires_in=obj_in.expires_in,
        user_id=obj_in.user_id,
        is_revoked=False
    )

    db.add(db_obj)
    db.commit()
    db.refresh(db_obj)

    return db_obj


def update_password(db: Session, new_password: str, user_id: str):
    user = user_services.get_user_by_id(db=db, user_id=user_id)

    if user.hashed_password:
        user.hashed_password = get_password_hash(new_password)

    db.add(user)
    db.commit()
    db.refresh(user)

    return user
