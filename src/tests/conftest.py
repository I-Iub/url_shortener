import datetime
import sys
from typing import AsyncGenerator, Callable

import asyncio
import pytest
import pytest_asyncio
from httpx import AsyncClient
from sqlalchemy import insert
from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine

from src.db.database import Base, get_session
from src.main import app
from src.models.urls import Pass, URL


@pytest.fixture(scope='session')
def event_loop():
    """
    Creates an instance of the default event loop for the test session.
    """
    if sys.platform.startswith("win") and sys.version_info[:2] >= (3, 8):
        # Avoid "RuntimeError: Event loop is closed" on Windows when tearing
        # down tests https://github.com/encode/httpx/issues/914
        asyncio.set_event_loop_policy(asyncio.WindowsSelectorEventLoopPolicy())

    loop = asyncio.new_event_loop()
    yield loop
    loop.close()


@pytest.fixture(scope='session')
def _database_url():
    return 'postgresql+asyncpg://postgres:postgres@localhost:65432/urls'


@pytest.fixture(scope='session')
def init_database():
    return Base.metadata.create_all


@pytest_asyncio.fixture(scope='session')
async def test_engine(_database_url):
    return create_async_engine(_database_url, echo=True)


@pytest_asyncio.fixture
async def test_app(db_session):
    async def override_get_db() -> AsyncGenerator[AsyncSession, None]:
        yield db_session

    app.dependency_overrides[get_session] = override_get_db
    return app


@pytest_asyncio.fixture
async def url_path_for(test_app) -> Callable:
    return test_app.url_path_for


@pytest_asyncio.fixture
async def client(test_app) -> AsyncGenerator[AsyncClient, None]:
    async with AsyncClient(app=test_app,
                           base_url='http://test.te') as async_client:
        yield async_client


@pytest_asyncio.fixture
async def create_url_and_pass(db_session: AsyncSession):
    url_records = [
        {'original': 'https://xyz.original.org/path0/path1',
         'short': '23230447fc1f360b19'},
        {'original': 'https://xyz.original.org/path0/path2',
         'short': '43220d474a1bf60ab6'},
        {'original': 'https://xyz.original.org/path0/path3',
         'short': '116e11dfffb7c1d5f1'},
        {'original': 'https://xyz.original.org/path0/path4',
         'short': '0cc3fb6c19e2c1f730',
         'deleted': True},
        {'original': 'https://xyz.original.org/path0/path5',
         'short': '8f7a675f2b54a804e5',
         'deleted': True},
    ]
    result = await db_session.execute(
        insert(URL).values(url_records).returning(URL.id)
    )
    date = datetime.datetime(2023, 2, 1, 12, 0)
    url_ids = result.scalars()
    for idx, url_id in enumerate(url_ids, start=1):
        pass_ = Pass(url_id=url_id,
                     time=date + datetime.timedelta(minutes=idx))
        db_session.add(pass_)
    await db_session.commit()


@pytest_asyncio.fixture
async def create_urls_with_many_passes(db_session: AsyncSession):
    url_records = [
        {'original': 'https://xyz.original.org/path0/path6',
         'short': '6b990563b16cbe9f07'},
    ]
    result = await db_session.execute(
        insert(URL).values(url_records).returning(URL.id)
    )
    url_id = result.scalar()
    for minute in range(10):
        pass_ = Pass(url_id=url_id,
                     time=datetime.datetime(2023, 2, 1, 13, minute))
        db_session.add(pass_)
    await db_session.commit()
