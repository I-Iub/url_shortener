from typing import Callable

import pytest
from fastapi import status

from httpx import AsyncClient
from src.api.v1.base import delete_url


@pytest.mark.parametrize('url', [
    'https://xyz.original.org/path0/path1',
    'https://xyz.original.org/path0/path5'  # deleted = True
])
async def test_post_existing_url(client: AsyncClient,
                                 url_path_for: Callable,
                                 create_url_and_redirects: Callable,
                                 url: str) -> None:
    response = await client.post(
        url_path_for(delete_url.__name__),
        json={'url': url}
    )
    assert response.status_code == status.HTTP_204_NO_CONTENT


async def test_post_non_existent_url(client: AsyncClient,
                                     url_path_for: Callable) -> None:
    response = await client.post(
        url_path_for(delete_url.__name__),
        json={'url': 'http://unexisting.url'}
    )
    assert response.status_code == status.HTTP_404_NOT_FOUND


async def test_incorrect_url(client: AsyncClient,
                             url_path_for: Callable) -> None:
    response = await client.post(
        url_path_for(delete_url.__name__),
        json={'url': 'incorrect_url'}
    )
    assert response.status_code == status.HTTP_422_UNPROCESSABLE_ENTITY
