from core.database.session import Session
from core.security import get_password_hash
from user import models, schemas
from user.models import User


def get_total_of_users(db: Session):
    return db.query(models.User).count()


def get_user_by_email(db: Session, email: str):
    return db.query(models.User).filter(models.User.email == email).first()


def get_user_by_id(db: Session, id: str) -> User:
    return db.query(models.User).filter(models.User.id == id).first()


def get_all_users(db: Session, skip: int = 0, limit: int = 100):
    return db.query(models.User).offset(skip).limit(limit).all()


def create_user(db: Session, user: schemas.UserCreate):
    new_entry = models.User(
        email=user.email,
        name=user.name,
        username=user.username,
        hashed_password=get_password_hash(user.password)
    )

    db.add(new_entry)
    db.commit()
    db.refresh(new_entry)

    return new_entry


# User Profile

def get_user_profile_by_user_id(db: Session, user_id: str):
    return db.query(models.UserProfile).filter(models.UserProfile.user_id == user_id).first()


def create_user_profile(db: Session, user_id: str, entry: schemas.UserProfileCreate):
    new_entry = models.UserProfile(
        user_id=user_id,
        expertises=entry.expertises,
        challenges=entry.challenges
    )

    db.add(new_entry)
    db.commit()
    db.refresh(new_entry)

    return new_entry
