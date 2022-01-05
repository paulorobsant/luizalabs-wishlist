from fastapi import Depends, HTTPException, APIRouter
from sqlalchemy.orm import Session
from starlette.responses import JSONResponse

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


@router.get("/{user_id}", response_model=schemas.UserRead, dependencies=[Depends(get_current_active_superuser)])
def read_user(user_id: str, db: Session = Depends(get_db)):
    db_user = services.get_user_by_id(db, user_id=user_id)

    if db_user is None:
        raise HTTPException(status_code=404, detail="User not found")

    return db_user


@router.delete("/{user_id}", response_model=schemas.UserRead, dependencies=[Depends(get_current_active_superuser)])
def delete_user(user_id: str, db: Session = Depends(get_db)):
    try:
        services.delete_user(db, user_id=user_id)

        return JSONResponse(status_code=200,
                            content={"message": "The operation was performed successfully."})
    except Exception as e:
        return HTTPException(status_code=404, detail=str(e))


@router.patch("/", response_model=schemas.UserRead, dependencies=[Depends(get_current_active_superuser)])
def update_user(entry: schemas.UserUpdate, db=Depends(get_db)):
    try:
        services.update_user(db, entry=entry)

        return JSONResponse(status_code=200,
                            content={"message": "The operation was performed successfully."})
    except Exception as e:
        return HTTPException(status_code=404, detail=str(e))
