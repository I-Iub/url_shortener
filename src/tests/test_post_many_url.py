from typing import Any, Callable

import pytest
from fastapi import status

from httpx import AsyncClient
from src.api.v1.base import post_many_url


async def test_post_new_valid_urls(client: AsyncClient,
                                   url_path_for: Callable) -> None:
    response = await client.post(
        url_path_for(post_many_url.__name__),
        json=[{'url': 'https://xyz.original.org/path0/path1'},
              {'url': 'https://xyz.original.org/path0/path2'}]
    )
    assert response.status_code == status.HTTP_201_CREATED


async def test_post_existing_urls(client: AsyncClient,
                                  url_path_for: Callable,
                                  create_url_and_pass: Callable) -> None:
    response = await client.post(
        url_path_for(post_many_url.__name__),
        json=[{'url': 'https://xyz.original.org/new'},
              {'url': 'https://xyz.original.org/path0/path1'},
              {'url': 'https://xyz.original.org/path0/path5'}]  # deleted=True
    )
    assert response.status_code == status.HTTP_201_CREATED


@pytest.mark.parametrize(
    'urls',
    [
        [{'url': 'incorrect_url'}, {'url': 'https://correct.org/new'}],
        [{'url': 1}, {'url': 'https://correct.org/new'}],
        {'not': 'list'}
    ]
)
async def test_post_incorrect_urls(client: AsyncClient,
                                   url_path_for: Callable,
                                   urls: Any) -> None:
    response = await client.post(
        url_path_for(post_many_url.__name__),
        json=urls
    )
    assert response.status_code == status.HTTP_422_UNPROCESSABLE_ENTITY
