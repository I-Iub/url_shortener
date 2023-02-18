import os
from typing import AsyncGenerator

import pytest_asyncio
from httpx import AsyncClient

from main import app


def setup_module() -> None:
    os.environ['SQLALCHEMY_DATABASE_URL'] = (
            'postgresql+asyncpg://postgres:postgres@localhost:35432/urls'  # ggggggggggggggggggg
    )


@pytest_asyncio.fixture
async def client() -> AsyncGenerator[AsyncClient, None]:
    async with AsyncClient(app=app, base_url="http://test") as async_client:
        yield async_client
