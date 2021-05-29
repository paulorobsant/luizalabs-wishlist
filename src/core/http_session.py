from fastapi import Depends, HTTPException
from fastapi.security import OAuth2PasswordBearer
from jose import jwt
from pydantic import ValidationError
from starlette import status

import settings as settings
from auth.schemas import TokenPayload
from core.database.deps import get_db
from core.database.session import Session
from user.models import User
from user.services import get_user_by_id

reusable_oauth2 = OAuth2PasswordBearer(tokenUrl=f"{settings.API_STR}/login/access_token")


def get_current_user(
        db: Session = Depends(get_db), token: str = Depends(reusable_oauth2)
):
    try:
        payload = jwt.decode(
            token, str(settings.SECRET_KEY), algorithms=[settings.ALGORITHM]
        )
        token_data = TokenPayload(**payload)
    except (jwt.JWTError, ValidationError):
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Could not validate credentials",
        )
    user = get_user_by_id(db=db, id=str(token_data.sub))

    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    return user


def get_current_active_user(
        current_user: User = Depends(get_current_user),
):
    if not current_user.is_active:
        raise HTTPException(status_code=400, detail="Inactive user")

    return current_user


def get_current_active_superuser(
        current_user: User = Depends(get_current_user),
):
    if not current_user.is_superuser:
        raise HTTPException(status_code=400, detail="The user does not have enough privileges")

    return current_user
