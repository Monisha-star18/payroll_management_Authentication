from collections.abc import AsyncGenerator
from sqlalchemy.ext.asyncio import ( async_sessionmaker,AsyncSession)
from app.database.connection import engine

#creating a session factory 
SessionLocal = async_sessionmaker( bind=engine ,
                            autoflush=True,
                            expire_on_commit=True
                        )

#dependecy creation 
async def get_session()-> AsyncGenerator[AsyncSession,None]:
    async with SessionLocal() as session :
        yield session