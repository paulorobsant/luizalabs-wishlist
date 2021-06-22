from fastapi import APIRouter
from user.endpoints import router as user_router
from match.endpoints import router as match_router
from auth.endpoints import router as login_router

router = APIRouter()

router.include_router(
    user_router,
    prefix="/users",
    tags=["Users"]
)

router.include_router(
    login_router,
    prefix="/login",
    tags=["Login"]
)

router.include_router(
    match_router,
    prefix="/matches",
    tags=["Match"]
)
