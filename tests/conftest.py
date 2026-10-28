import os
from dotenv import load_dotenv
from fastapi.testclient import TestClient
import pytest
from sqlalchemy.ext.asyncio import create_async_engine,async_sessionmaker

from main import app
from app.database.connection import get_session

load_dotenv()

TEST_DATABASE_URL = os.getenv('TEST_DATABASE_URL')

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

# Override function the original session dependency
async def override_get_session():
    async with TestingSessionLocal() as session :
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




