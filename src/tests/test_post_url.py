from typing import Any, Callable

import pytest
from fastapi import status
from httpx import AsyncClient

from src.api.v1.base import post_url


@pytest.mark.parametrize(
    'url, expected',
    [('https://xyz.original.org/path1/path1', '1b2324d6583610d4d5'),
     ('https://xyz.original.org/path1/path2', 'f3dfd9d8b5213bed48')])
async def test_post_correct_url(client: AsyncClient,
                                url_path_for: Callable,
                                url: str,
                                expected: str) -> None:
    response = await client.post(url_path_for(post_url.__name__),
                                 json={'url': url})
    assert response.json() == {'short_url_id': expected}
    assert response.status_code == status.HTTP_201_CREATED


@pytest.mark.parametrize(
    'url, expected',
    [('https://xyz.original.org/path0/path1', '23230447fc1f360b19'),
     # post url where deleted = True:
     ('https://xyz.original.org/path0/path5', '8f7a675f2b54a804e5')]
)
async def test_post_existing_url(client: AsyncClient,
                                 url_path_for: Callable,
                                 url: str,
                                 expected: str,
                                 create_url_and_redirects: Callable) -> None:
    response = await client.post(url_path_for(post_url.__name__),
                                 json={'url': url})
    assert response.status_code == status.HTTP_201_CREATED
    assert response.json() == {'short_url_id': expected}


@pytest.mark.parametrize('url', ['incorrect_url', 1, {}, None])
async def test_post_incorrect_url_incorrect_url(client: AsyncClient,
                                                url_path_for: Callable,
                                                url: Any) -> None:
    response = await client.post(url_path_for(post_url.__name__),
                                 json={'url': url})
    assert response.status_code == status.HTTP_422_UNPROCESSABLE_ENTITY
