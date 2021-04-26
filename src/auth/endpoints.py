from datetime import timedelta

from fastapi import APIRouter, Depends, Request, HTTPException
from fastapi.security import OAuth2PasswordRequestForm
from starlette import status

import settings as settings
from auth import schemas
from auth.services import authenticate, save_login_attempt
from company import services as company_services
from company.utils import get_email_suffix
from core import security
from core.database.deps import get_db
from core.database.session import Session
from user import services as user_services, schemas as user_schemas

router = APIRouter()


@router.post("/register", response_model=user_schemas.UserRead)
def register(*, entry: schemas.UserRegister, db: Session = Depends(get_db)):
    db_user = user_services.get_user_by_email(db, email=entry.email)

    if db_user:
        raise HTTPException(status_code=400, detail="Email already registered")

    email_suffix = get_email_suffix(email=entry.email)
    db_company = company_services.get_company_by_email_suffix(db=db, email_suffix=email_suffix)

    if not db_company:
        raise HTTPException(status_code=400, detail="It was not possible to register. Your company is not part of our "
                                                    "platform.")

    entry = user_schemas.UserCreate(**{
        "name": entry.name,
        "email": entry.email,
        "username": entry.username,
        "password": entry.password
    })

    user = user_services.create_user(db=db, user=entry)
    company_services.attach_user_to_company(db=db, user_id=user.id, company_id=db_company.id)

    return user


@router.post("/access_token", response_model=schemas.Token)
def login_access_token(
        db: Session = Depends(get_db),
        form_data: OAuth2PasswordRequestForm = Depends(),
        request: Request = None
):
    """
    OAuth2 compatible token login, get an access token for future requests
    """
    user = authenticate(db, username=form_data.username, password=form_data.password)

    if not user:
        save_login_attempt(
            db=db,
            request=request,
            email_or_username=form_data.username,
            description="A user tried to access an account that does not exist or entered incorrect credentials."
        )

        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Incorrect username or password")
    elif not user.is_active:
        save_login_attempt(
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
