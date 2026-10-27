from fastapi import APIRouter, Depends
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.ext.asyncio import AsyncSession

from app.database.connection import get_session
from app.dependency.auth import get_current_user
from app.dependency.dependency import get_auth_service
from app.models.User_Model import User
from app.schemas.auth_schema import RegisterRequest, TokenResponse, UserResponse
from app.services.implementation.auth_service import AuthService

router = APIRouter(prefix="/api/auth", tags=["Auth"])


@router.post("/register",
             response_model=UserResponse,
            )
async def register(body: RegisterRequest,
                   db: AsyncSession = Depends(get_session),
                   service: AuthService = Depends(get_auth_service)
                ):
    return await service.register(body, db)


@router.post("/login",
            response_model=TokenResponse
            )
async def login(form: OAuth2PasswordRequestForm = Depends(),
                db: AsyncSession = Depends(get_session),
                service: AuthService = Depends(get_auth_service)
            ):
    return await service.login(form.username, form.password, db) 


@router.get("/me", response_model=UserResponse)
async def me(user: User = Depends(get_current_user)):
    return user

