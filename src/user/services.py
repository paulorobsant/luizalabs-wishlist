from core.database.session import Session
from core.security import get_password_hash
from core.utils import from_schema_to_model
from user import models, schemas
from user.models import User


def get_user_by_email(db: Session, email: str):
    return db.query(models.User).filter(models.User.email == email).first()


def get_user_by_id(db: Session, user_id: str) -> User:
    return db.query(models.User).filter(models.User.id == user_id).first()


def create_user(db: Session, user: schemas.UserCreate):
    new_entry = models.User(
        email=user.email,
        name=user.name,
        hashed_password=get_password_hash(user.password)
    )

    db.add(new_entry)
    db.commit()
    db.refresh(new_entry)

    return new_entry


def delete_user(db: Session, user_id: str):
    entry = db.query(models.User).filter(models.User.id == user_id).first()

    if not entry:
        raise Exception("User not found.")

    db.delete(entry)
    db.commit()


def update_user(db: Session, entry: schemas.UserUpdate):
    current_entry = db.query(models.User).filter(models.User.id == entry.id).first()

    if not current_entry:
        raise Exception("User not found.")

    new_entry = from_schema_to_model(schema=entry, model=current_entry)

    db.add(new_entry)
    db.commit()
    db.refresh(new_entry)
