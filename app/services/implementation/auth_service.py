import jwt
from fastapi import HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.security import (create_access_token, decode_access_token,
                               hash_password, verify_password)
from app.models.User_Model import User
from app.repositories.interface.user_repo_interface import UserRepoInterface
from app.schemas.auth_schema import RegisterRequest, TokenResponse


class AuthService:

    def __init__(self, user_repository: UserRepoInterface) -> None:
        self.user_repository = user_repository

    async def register(self,
        body: RegisterRequest,
        db: AsyncSession
        ) -> User:

        if await self.user_repository.get_by_username(body.username, db):
            raise HTTPException(status.HTTP_400_BAD_REQUEST, "Username already taken")

        # public signup is ALWAYS "user"
        return await self.user_repository.create_user(
            body.username, hash_password(body.password), "user", db)

    async def login(self,
        username: str,
        password: str,
        db: AsyncSession
        ) -> TokenResponse:

        user = await self.user_repository.get_by_username(username, db)

        if not user or not verify_password(password, user.hashed_password):
            raise HTTPException(status.HTTP_401_UNAUTHORIZED,
                                "Incorrect username or password",
                                headers={"WWW-Authenticate": "Bearer"})

        return TokenResponse(access_token=create_access_token(user.username, user.role))

    async def get_user_from_token(self,
        token: str,
        db: AsyncSession
        ) -> User:

        credentials_error = HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid or expired token",
            headers={"WWW-Authenticate": "Bearer"})

        try:
            username = decode_access_token(token).get("sub")
        except jwt.PyJWTError:
            raise credentials_error

        if not username:
            raise credentials_error

        user = await self.user_repository.get_by_username(username, db)
        if user is None:
            raise credentials_error
        return user