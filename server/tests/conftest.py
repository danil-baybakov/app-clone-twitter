import asyncio
from typing import AsyncGenerator

import pytest
from config import setting
from fastapi.testclient import TestClient
from httpx import AsyncClient
from sqlalchemy import insert, text
from sqlalchemy.ext.asyncio import (
    AsyncSession,
    async_sessionmaker,
    create_async_engine,
)
from sqlalchemy.pool import NullPool

from app.db.db import get_async_session
from app.main import app
from app.models.base import metadata
from app.utils.generate import USERS

from app.models.users import User


engine_test = create_async_engine(
    setting.database_test_url_asyncpg, poolclass=NullPool, echo=True
)
async_session_maker = async_sessionmaker(
    engine_test, class_=AsyncSession, expire_on_commit=False
)

metadata.bind = engine_test


async def override_get_async_session() -> AsyncGenerator[AsyncSession, None]:
    async with async_session_maker() as session:
        yield session


app.dependency_overrides[get_async_session] = override_get_async_session


@pytest.fixture(autouse=True, scope="session")
async def prepare_database():
    async with engine_test.begin() as conn:
        await conn.run_sync(metadata.create_all)
        stmt = insert(User).values(USERS)
        await conn.execute(stmt)
        await conn.commit()
    yield
    async with engine_test.begin() as conn:
        await conn.run_sync(metadata.drop_all)


@pytest.fixture(scope="function")
async def async_db():
    async with async_session_maker() as session:
        await session.begin()

        stmt = insert(User).values(USERS)
        await session.execute(stmt)
        await session.commit()

        yield session
        await session.rollback()

        for table in reversed(metadata.sorted_tables):
            stmt = text(f"TRUNCATE {table.name} CASCADE; ")
            await session.execute(stmt)
            await session.commit()


# SETUP
@pytest.fixture(scope="session")
def event_loop(request):
    """Create an instance of the default event loop for each test case."""
    loop = asyncio.get_event_loop_policy().new_event_loop()
    yield loop
    loop.close()


client = TestClient(app)


@pytest.fixture(scope="session")
async def ac() -> AsyncGenerator[AsyncClient, None]:
    headers = {
        "api-key": f"{USERS[1]['api_key']}",
        "accept": "application/json",
    }
    async with AsyncClient(
        app=app,
        base_url=f"http://{setting.HOST}:{setting.PORT}{setting.BASE_URI}",
        headers=headers,
    ) as ac:
        yield ac
