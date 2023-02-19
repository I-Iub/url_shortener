import os
from typing import AsyncGenerator

import pytest_asyncio
from httpx import AsyncClient

from src.main import app


def setup_module() -> None:
    os.environ['DSN'] = (
        'postgresql+asyncpg://postgres:postgres@localhost:5432/urls'
    )


@pytest_asyncio.fixture
async def client() -> AsyncGenerator[AsyncClient, None]:
    async with AsyncClient(app=app, base_url="http://test") as async_client:
        yield async_client
