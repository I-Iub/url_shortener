import orjson

import pytest
from fastapi import status
from httpx import AsyncClient


@pytest.mark.asyncio
async def test_post_correct_url(client: AsyncClient):
    response = await client.post(
        '/api/v1/',
        content=orjson.dumps({'url': 'https://xyz.original.org/path1/path2'})
    )
    assert response.status_code == status.HTTP_201_CREATED
    assert response.json().get('short_url_id') == 'f3dfd9d8b5213bed48'


@pytest.mark.asyncio
async def test_post_incorrect_url(client: AsyncClient):
    response = await client.post(
        '/api/v1/',
        content=orjson.dumps({'url': 'incorrect_url'})
    )
    assert response.status_code == status.HTTP_422_UNPROCESSABLE_ENTITY
