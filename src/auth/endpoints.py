import auth.services as auth_services
import settings as settings

from datetime import timedelta
from fastapi import APIRouter, Depends, Request, HTTPException
from fastapi.security import OAuth2PasswordRequestForm
from starlette import status
from starlette.responses import JSONResponse
from auth import schemas
from core import security
from core.database.deps import get_db
from core.database.session import Session
from core.http_session import get_current_active_user
from user import services as user_services, schemas as user_schemas
from user.models import User

router = APIRouter()


@router.post("/register", response_model=user_schemas.UserRead)
def register(*, entry: schemas.UserRegister, db: Session = Depends(get_db)):
    try:
        db_user = user_services.get_user_by_email(db, email=entry.email)

        if db_user:
            return JSONResponse(status_code=400, content={"message": "Email already registered."})

        entry = user_schemas.UserCreate(**{
            "name": entry.name,
            "email": entry.email,
            "password": entry.password
        })

        user_services.create_user(db=db, user=entry)

        return JSONResponse(status_code=200, content={"message": "Your registration was successful."})
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail={"message": "Oops! Something went wrong. "
                                                                                        "Try later."})


@router.post("/access_token", response_model=schemas.Token)
def login_access_token(
        form_data: OAuth2PasswordRequestForm = Depends(),
        db: Session = Depends(get_db),
        request: Request = None
):
    """
    OAuth2 compatible token login, get an access token for future requests
    """
    user = auth_services.authenticate(db, email=form_data.username, password=form_data.password)

    if not user:
        auth_services.save_login_attempt(
            db=db,
            request=request,
            email_or_username=form_data.username,
            description="A user tried to access an account that does not exist or entered incorrect credentials."
        )

        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Wrong credentials.")
    elif not user.is_active:
        auth_services.save_login_attempt(
            db=db, request=request,
            email_or_username=form_data.username,
            description="A user tried to access an inactive account."
        )

        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Inactive user")

    access_token_expires = timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)

    return {
        "access_token": security.create_access_token(user.id, expires_delta=access_token_expires),
        "token_type": "Bearer",
    }


@router.get("/me", response_model=schemas.UserAuthenticated)
def read_me(current_user: User = Depends(get_current_active_user)):
    return current_user
