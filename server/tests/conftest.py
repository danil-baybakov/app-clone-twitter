import asyncio
import os
from typing import AsyncGenerator

import pytest
from config import setting
from fastapi.testclient import TestClient
from httpx import ASGITransport, AsyncClient
from sqlalchemy import func, insert, select, text
from sqlalchemy.ext.asyncio import AsyncSession

os.environ["ENV"] = "test"  # noqa
from db.db import Base, async_session_maker, engine  # noqa
from models.followers import Follower  # noqa
from models.likes import Like  # noqa
from models.medias import Media  # noqa
from models.tweets import Tweet  # noqa
from models.users import User  # noqa

from app.main import app  # noqa
from app.models.base import metadata  # noqa
from app.utils.fake_data import (  # noqa
    FOLLOWERS,
    LIKES,
    MEDIAS,
    TWEETS,
    USERS,
    mock_image,
    rand_image,
)

#######################################


@pytest.fixture(autouse=True, scope="session")
async def prepare_database():
    async with engine.begin() as conn:
        await conn.run_sync(metadata.create_all)
    yield
    async with engine.begin() as conn:
        await conn.run_sync(metadata.drop_all)


@pytest.fixture(autouse=True, scope="function")
async def async_db():
    async with async_session_maker() as session:
        await session.begin()

        yield session

        await session.commit()

        await session.rollback()

        for table in reversed(metadata.sorted_tables):
            stmt = text(f"TRUNCATE {table.name} CASCADE; ")
            await session.execute(stmt)
            await session.commit()
            stmt = text(f"ALTER SEQUENCE {table.name}_id_seq RESTART WITH 1;")
            await session.execute(stmt)
            await session.commit()


async def add_items_table_db(
    session: AsyncSession, model: Base, items: list[dict[str, any]]
):
    stmt = insert(model).values(items)
    await session.execute(stmt)
    await session.commit()


@pytest.fixture(scope="function")
async def prepare_gen_full_tables_db(async_db: AsyncSession):
    await add_items_table_db(async_db, User, USERS)
    await add_items_table_db(async_db, Tweet, TWEETS)
    await add_items_table_db(async_db, Media, MEDIAS)
    await add_items_table_db(async_db, Like, LIKES)
    await add_items_table_db(async_db, Follower, FOLLOWERS)


@pytest.fixture(scope="function")
async def prepare_gen_only_user_table_db(async_db: AsyncSession):
    await add_items_table_db(async_db, User, USERS)


#######################################

#######################################
client = TestClient(app)


@pytest.fixture(scope="function")
async def ac() -> AsyncGenerator[AsyncClient, None]:
    headers = {
        "api-key": f"{USERS[0]['api_key']}",
        "accept": "application/json",
    }
    async with AsyncClient(
        transport=ASGITransport(app=app),
        base_url=f"http://{setting.HOST}:{setting.PORT}{setting.BASE_URI}",
        headers=headers,
    ) as ac:
        yield ac


#######################################


#######################################
# SETUP
@pytest.fixture(scope="session")
def event_loop(request):
    """Create an instance of the default event loop for each test case."""
    loop = asyncio.get_event_loop_policy().new_event_loop()
    yield loop
    loop.close()


#######################################


@pytest.fixture
async def gen_medias_db(async_db: AsyncSession):
    medias = []
    for i in range(3):
        stmt = (
            insert(Media)
            .values(file_name=f"img_{i}", file_body=mock_image(rand_image))
            .returning(Media)
        )
        res = await async_db.execute(stmt)
        await async_db.commit()
        medias.append(res.scalar_one())
    return medias


async def get_last_row_id_db(session: AsyncSession, model: Base) -> int | None:
    stmt = select(model).order_by(model.id.desc()).limit(1)
    result = await session.execute(stmt)
    res = result.scalars().one_or_none()
    if res is not None:
        return res.id


async def check_row_table_db(
    session: AsyncSession, model: Base, **kwargs
) -> int | None:
    stmt = select(model).filter_by(**kwargs)
    res = await session.execute(stmt)
    rows = res.scalars().all()
    return len([row for row in rows]) > 0


async def get_count_row_db(session: AsyncSession, model: Base) -> int | None:
    stmt = select(func.count(model.id))
    result = await session.execute(stmt)
    return result.scalars().one()


async def check_is_set_tweet_id_medias_db(
    session: AsyncSession, ids: list[int], id: int | None = None
):
    session.expire_all()
    stmt = select(Media).filter(Media.id.in_(ids))
    res = await session.execute(stmt)
    return any(media.tweet_id == id for media in res.scalars().all())
