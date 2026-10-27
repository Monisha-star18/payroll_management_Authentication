from typing import Optional
from fastapi import HTTPException
from sqlalchemy import select
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.User_Model import User
from app.repositories.interface.user_repo_interface import UserRepoInterface


class UserRepo(UserRepoInterface):

    async def get_by_username(self,
        username: str,
        db: AsyncSession
        ) -> Optional[User]:

        try:
            result = await db.execute(select(User).where(User.username == username))
            return result.scalar_one_or_none()
        
        except SQLAlchemyError as er:
            raise HTTPException(status_code=500, detail=str(er))

    async def create_user(self,
        username: str,
        hashed_password: str,
        role: str,
        db: AsyncSession
        ) -> User:

        try:
            user = User(username=username,
                        hashed_password=hashed_password,
                        role=role)
            db.add(user)
            await db.commit()
            await db.refresh(user)
            return user
        
        except SQLAlchemyError as er:
            await db.rollback()
            raise HTTPException(status_code=500, detail=str(er))