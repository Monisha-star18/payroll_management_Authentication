from sqlalchemy.ext.asyncio import AsyncEngine, create_async_engine

from app.core.config import get_settings

setting = get_settings()

if not setting.database_url :
    raise RuntimeError("DATABASE_URL is not set. Check your .env file.")

#create a new engine 
engine:AsyncEngine = create_async_engine ( 
                        setting.database_url , 
                        pool_size= 5,
                        pool_timeout=30,
                        pool_recycle=1800,
                        pool_pre_ping= True,
                        echo= False 
                    )

