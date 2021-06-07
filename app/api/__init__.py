from fastapi import APIRouter

from app.api.endpoints import healthcheck, login, user

api_router = APIRouter()
api_router.include_router(
    healthcheck.router, prefix="/healthcheck", tags=["Healthcheck"]
)
api_router.include_router(login.router, prefix="/login", tags=["Login"])
api_router.include_router(user.router, prefix="/user", tags=["Users"])
