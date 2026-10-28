from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from sqlalchemy.ext.asyncio import AsyncSession

from app.database.connection import get_session
from app.api.dependency.dependency import get_auth_service
from app.models.User_Model import User
from app.services.implementation.auth_service import AuthService

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/api/auth/login")


async def get_current_user(token: str = Depends(oauth2_scheme),
                           db: AsyncSession = Depends(get_session),
                           service: AuthService = Depends(get_auth_service)
                           ) -> User:
    return await service.get_user_from_token(token, db)


def require_roles(*allowed_roles: str):
    async def checker(user: User = Depends(get_current_user)) -> User:
        if user.role not in allowed_roles:
            raise HTTPException(status.HTTP_403_FORBIDDEN,
                                detail="You do not have permission for this action")
        return user
    return checker