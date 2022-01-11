from fastapi import Depends, APIRouter
from sqlalchemy.orm import Session
from starlette.responses import JSONResponse
from core.database.deps import get_db
from core.http_session import get_current_user
from user import schemas, services
from starlette import status

router = APIRouter()


# User

# @router.post("/", response_model=schemas.UserRead)
# def create_user(*, entry: schemas.UserCreate, db: Session = Depends(get_db)):
#     try:
#         db_user = services.get_user_by_email(db, email=entry.email)
#
#         if db_user:
#             return JSONResponse(status_code=status.HTTP_400_BAD_REQUEST,
#                                 content={"message": "Email already registered."})
#
#         services.create_user(db=db, user=entry)
#
#         return JSONResponse(status_code=status.HTTP_200_OK,
#                             content={"message": "User has been registered successfully."})
#
#     except Exception as e:
#         return JSONResponse(status_code=status.HTTP_400_BAD_REQUEST, content={"message": f"{e}"})
#

@router.get("/{user_id}", response_model=schemas.UserRead, dependencies=[Depends(get_current_user)])
def read_user(user_id: str, db: Session = Depends(get_db)):
    db_user = services.get_user_by_id(db, user_id=user_id)

    if db_user is None:
        return JSONResponse(status_code=status.HTTP_400_BAD_REQUEST, content={"message": "User not found."})

    return db_user


@router.delete("/{user_id}", response_model=schemas.UserRead, dependencies=[Depends(get_current_user)])
def delete_user(user_id: str, db: Session = Depends(get_db)):
    try:
        services.delete_user(db, user_id=user_id)

        return JSONResponse(status_code=200,
                            content={"message": "User has been deleted successfully"})
    except Exception as e:
        return JSONResponse(status_code=status.HTTP_400_BAD_REQUEST, content={"message": f"{e}"})


@router.patch("/", response_model=schemas.UserRead, dependencies=[Depends(get_current_user)])
def update_user(entry: schemas.UserUpdate, db=Depends(get_db)):
    try:
        db_user = services.get_user_by_id(db, user_id=entry.id)

        if not db_user:
            return JSONResponse(status_code=status.HTTP_400_BAD_REQUEST,
                                content={"message": "User not found."})

        services.update_user(db, entry=entry)

        return JSONResponse(status_code=200,
                            content={"message": "User has been updated successfully"})
    except Exception as e:
        return JSONResponse(status_code=status.HTTP_400_BAD_REQUEST, content={"message": f"{e}"})
