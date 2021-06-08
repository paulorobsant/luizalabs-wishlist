import datetime
import json
from datetime import timedelta

import jwt
from fastapi import APIRouter, Depends, Request, HTTPException
from fastapi.security import OAuth2PasswordRequestForm
from starlette import status
from starlette.responses import JSONResponse

import auth.services as auth_services
import settings as settings
from auth import schemas
from auth.emails import send_reset_password_email
from company import services as company_services
from company.utils import get_email_suffix
from core import security
from core.database.deps import get_db
from core.database.session import Session
from core.http_session import get_current_active_superuser, get_current_active_user
from core.security import create_access_token
from user import services as user_services, schemas as user_schemas
from user.models import User

router = APIRouter()


@router.post("/register", response_model=user_schemas.UserRead)
def register(*, entry: schemas.UserRegister, db: Session = Depends(get_db)):
    try:
        db_user = user_services.get_user_by_email(db, email=entry.email)

        if db_user:
            return JSONResponse(status_code=400, content={"message": "Email already registered."})

        db_company = company_services.get_company_by_email_suffix(db=db,
                                                                  email_suffix=get_email_suffix(email=entry.email))

        if entry.code:
            # Decode the JWT token

            decode = jwt.decode(jwt=entry.code, key=str(settings.SECRET_KEY), algorithms=[settings.ALGORITHM])

            # Convert the sub data
            exp_data = decode.get("exp")
            sub_data = decode.get("sub")
            sub_data = json.loads(sub_data)

            # Token Data
            token_company_id = sub_data["company_id"]
            token_email = sub_data["email"]

            if not decode:
                return JSONResponse(status_code=400,
                                    content={
                                        "message": "It was not possible to register. Your code invitation is not valid."})

            if (datetime.datetime.fromtimestamp(exp_data) - datetime.datetime.now()).days > 2:
                return JSONResponse(status_code=400,
                                    content={"message": "The registration invitation code has expired."})

            if token_email != entry.email:
                return JSONResponse(status_code=400,
                                    content={"message": "It was not possible to register. Your email is not valid."})

            if not token_company_id:
                return JSONResponse(status_code=400,
                                    content={
                                        "message": "It was not possible to register. Your invitation is not tied to a group."})

            # Find company by ID
            db_company = company_services.get_company_by_id(db=db, id=token_company_id)

        if not db_company:
            return JSONResponse(status_code=400,
                                content={"message": "It was not possible to register. Your company is not part of our "
                                                   "platform."})

        entry = user_schemas.UserCreate(**{
            "name": entry.name,
            "email": entry.email,
            "username": entry.username,
            "password": entry.password
        })

        user = user_services.create_user(db=db, user=entry)
        company_services.attach_user_to_company(db=db, user_id=user.id, company_id=db_company.id)

        return JSONResponse(status_code=200, content={"message": "Your registration was successful."})
    except Exception:
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
    user = auth_services.authenticate(db, username=form_data.username, password=form_data.password)

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


@router.post("/create_invitation", dependencies=[Depends(get_current_active_superuser)])
def create_invitation(*, entry: schemas.UserInvitation):
    try:
        # Generate token
        subject = json.dumps({"company_id": entry.company_id, "email": entry.email})
        expires_delta = datetime.timedelta(hours=48)
        code = create_access_token(subject=subject, expires_delta=expires_delta)

        return JSONResponse(status_code=200, content={"message": "The invitation code was successfully generated.",
                                                      "data": code.decode("utf-8")})
    except:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Inactive user")


@router.post("/forgot_password")
def forgot_password(*, entry: schemas.UserForgotPassword, db: Session = Depends(get_db)):
    try:
        user = user_services.get_user_by_email(db=db, email=entry.email)

        # Generate token
        subject = json.dumps({"email": entry.email})
        expires_delta = datetime.timedelta(hours=24)
        code = create_access_token(subject=subject, expires_delta=expires_delta)

        if user:
            send_reset_password_email(email_to=entry.email, name=user.name, code=code.decode("utf-8"))

        return JSONResponse(status_code=200, content={"message": "If your email is registered in the system then you "
                                                                 "will receive an email in a few minutes."})
    except:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,
                            detail="It was not possible to perform the operation.")


@router.post("/reset_password")
def reset_password(*, entry: schemas.UserResetPassword, db: Session = Depends(get_db)):
    try:
        # Decode the JWT token
        decode = jwt.decode(jwt=entry.code, key=str(settings.SECRET_KEY), algorithms=[settings.ALGORITHM])

        # Convert the sub data
        sub_data = decode.get("sub")
        sub_data = json.loads(sub_data)

        user = user_services.get_user_by_email(db=db, email=sub_data["email"])
        auth_services.update_password(db=db, new_password=entry.password, user_id=user.id)

        return JSONResponse(status_code=200, content={"message": "The password was successfully reset."})
    except:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,
                            detail="It was not possible to perform the operation.")


@router.get("/me", response_model=schemas.UserAuthenticated)
def read_me(current_user: User = Depends(get_current_active_user)):
    return current_user
