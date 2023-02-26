from typing import Callable

import pytest
from fastapi import status

from httpx import AsyncClient
from src.api.v1.base import get_original_url


@pytest.mark.parametrize(
    'short_url_id, expected',
    [('23230447fc1f360b19', {'url': 'https://xyz.original.org/path0/path1'}),
     ('43220d474a1bf60ab6', {'url': 'https://xyz.original.org/path0/path2'})]
)
async def test_get_existing_url(client: AsyncClient,
                                url_path_for: Callable,
                                create_url_and_pass: Callable,
                                short_url_id: str,
                                expected: dict) -> None:
    response = await client.get(
        url_path_for(get_original_url.__name__, short_url_id=short_url_id)
    )
    assert response.status_code == status.HTTP_307_TEMPORARY_REDIRECT
    assert response.json() == expected


async def test_get_non_existing_url(client: AsyncClient,
                                    url_path_for: Callable) -> None:
    response = await client.get(url_path_for(
        get_original_url.__name__,
        short_url_id='not_exists'
    ))
    assert response.status_code == status.HTTP_404_NOT_FOUND


async def test_get_deleted_url(client: AsyncClient,
                               url_path_for: Callable,
                               create_url_and_pass: Callable) -> None:
    response = await client.get(url_path_for(
        get_original_url.__name__,
        short_url_id='0cc3fb6c19e2c1f730'
    ))
    assert response.status_code == status.HTTP_410_GONE
