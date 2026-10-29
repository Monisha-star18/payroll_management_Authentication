import asyncio

import pytest
from fastapi.testclient import TestClient
from sqlalchemy.ext.asyncio import async_sessionmaker, create_async_engine

from app.core.config import get_settings
from app.database.base import Base
from app.database.session import get_session
from main import app

setting = get_settings()

TEST_DATABASE_URL = setting.test_database_url

if not TEST_DATABASE_URL:
    raise RuntimeError(
        "TEST_DATABASE_URL is not configured"
    )


test_engine = create_async_engine(
    url=TEST_DATABASE_URL,
    echo=False
)

TestingSessionLocal = async_sessionmaker(
    bind=test_engine,
    autoflush=False,
    expire_on_commit=False
)



# Create and delete tables automatically
@pytest.fixture(scope="session", autouse=True)
def setup_test_database():

    async def create_tables():
        async with test_engine.begin() as conn:
            await conn.run_sync(Base.metadata.create_all)

    async def delete_tables():
        async with test_engine.begin() as conn:
            await conn.run_sync(Base.metadata.drop_all)

        await test_engine.dispose()

    asyncio.run(create_tables())

    try:
        yield
    finally:
        asyncio.run(delete_tables())


# Override the real database session
async def override_get_session():
    async with TestingSessionLocal() as session:
        yield session


@pytest.fixture
def client():

    #this is a dictory
    app.dependency_overrides[get_session] = (override_get_session)

    try:
        with TestClient(app) as testclient :
            yield testclient

    finally:
        app.dependency_overrides.pop(get_session,None)




