from core.database.session import Session
from core.security import get_password_hash
from core.security import verify_password
from auth import schemas
from auth.models import Token
from fastapi import Request
from user.models import User, UserLoginAttemptsLog


def save_login_attempt(db: Session, request: Request, email_or_username: str, description):
    login_attempt = UserLoginAttemptsLog(
        browser_info=request.headers.get("user-agent"),
        client_ip_address=request.client.host,
        client_name=None,
        email_or_username=email_or_username,
        description=description
    )

    db.add(login_attempt)
    db.commit()
    db.refresh(login_attempt)


def authenticate(db: Session, username: str, password: str):
    db_user = db.query(User).filter(User.username == username).first()

    if not db_user:
        return None

    if not verify_password(password, db_user.hashed_password):
        return None

    return db_user


def register(db: Session, obj_in: schemas.UserRegister):
    db_obj = User(
        email=obj_in.email,
        hashed_password=get_password_hash(obj_in.password),
        username=obj_in.username,
        name=obj_in.name,
        is_superuser=False,
        role_id=obj_in.role_id,
        is_active=True
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
