from typing import List

from fastapi import Depends, HTTPException, APIRouter
from sqlalchemy.orm import Session

from core.database.deps import get_db
from core.http_session import get_current_active_superuser
from user import schemas, services

router = APIRouter()


# User

@router.post("/", response_model=schemas.UserRead, dependencies=[Depends(get_current_active_superuser)])
def create_user(*, entry: schemas.UserCreate, db: Session = Depends(get_db)):
    db_user = services.get_user_by_email(db, email=entry.email)

    if db_user:
        raise HTTPException(status_code=400, detail="Email already registered")

    return services.create_user(db=db, user=entry)


@router.get("/", response_model=List[schemas.UserRead], dependencies=[Depends(get_current_active_superuser)])
def read_all_users(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    users = services.get_all_users(db, skip=skip, limit=limit)
    return users


@router.get("/{user_id}", response_model=schemas.UserRead, dependencies=[Depends(get_current_active_superuser)])
def read_user(user_id: str, db: Session = Depends(get_db)):
    db_user = services.get_user_by_id(db, id=user_id)

    if db_user is None:
        raise HTTPException(status_code=404, detail="User not found")

    return db_user


# User Profile

@router.post("/{user_id}/profile/", response_model=schemas.UserProfileRead, dependencies=[Depends(get_current_active_superuser)])
def create_user_profile(*, user_id: str, entry: schemas.UserProfileCreate, db: Session = Depends(get_db)):
    db_user_profile = services.get_user_profile_by_user_id(db, user_id=user_id)

    if db_user_profile:
        raise HTTPException(status_code=400, detail="The user profile is already registered.")

    return services.create_user_profile(db=db, user_id=user_id, entry=entry)


@router.get("/{user_id}/profile/", response_model=schemas.UserProfileRead, dependencies=[Depends(get_current_active_superuser)])
def read_user_profile(user_id: str, db: Session = Depends(get_db)):
    db_user_profile = services.get_user_profile_by_user_id(db, user_id=user_id)

    if db_user_profile is None:
        raise HTTPException(status_code=404, detail="User profile not found.")

    return db_user_profile
