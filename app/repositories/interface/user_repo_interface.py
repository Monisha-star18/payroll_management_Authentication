from abc import ABC, abstractmethod
from typing import Optional
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.User_Model import User


class UserRepoInterface(ABC):

    @abstractmethod
    async def get_by_username(self,
        username: str,
        db: AsyncSession
        ) -> Optional[User]:
        pass

    @abstractmethod
    async def create_user(self,
        username: str,
        hashed_password: str,
        role: str,
        db: AsyncSession
        ) -> User:
        pass