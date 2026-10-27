import os 
from collections.abc import AsyncGenerator
from dotenv import load_dotenv
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.asyncio import AsyncEngine, create_async_engine , async_sessionmaker,AsyncSession

load_dotenv()

DATABASE_URL:str|None = os.getenv("DATABASE_URL")

if not DATABASE_URL :
    raise RuntimeError("DATABASE_URL is not set. Check your .env file.")

#create a new engine 
engine:AsyncEngine = create_async_engine ( DATABASE_URL , 
                        pool_size= 5,
                        pool_timeout=30,
                        pool_recycle=1800,
                        pool_pre_ping= True,
                        echo= False 
                    )

#creating a session factory 
SessionLocal = async_sessionmaker( bind=engine ,
                            autoflush=True,
                            expire_on_commit=True
                        )

#dependecy creation 
async def get_session()-> AsyncGenerator[AsyncSession,None]:
    async with SessionLocal() as session :
        yield session
