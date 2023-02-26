from typing import Callable

from fastapi import status
from httpx import AsyncClient

from src.api.v1.base import get_status


async def test_get_existing_url_status(
        client: AsyncClient,
        url_path_for: Callable,
        create_url_and_redirects: Callable,
        create_urls_with_many_redirects: Callable
) -> None:
    response = await client.get(url_path_for(
        get_status.__name__,
        short_url_id='23230447fc1f360b19'
    ))
    assert response.status_code == status.HTTP_200_OK
    assert response.json().get('redirects') == 1
    assert response.json().get('times') is None

    response = await client.get(url_path_for(
        get_status.__name__,
        short_url_id='6b990563b16cbe9f07'
    ))
    assert response.status_code == status.HTTP_200_OK
    assert response.json().get('redirects') == 10
    assert response.json().get('times') is None

    response = await client.get(
        url_path_for(
            get_status.__name__,
            short_url_id='6b990563b16cbe9f07',
        ),
        params={'full_info': True}
    )
    assert response.status_code == status.HTTP_200_OK
    assert response.json().get('redirects') == 10
    assert response.json().get('times') == ['2023-02-01T13:00:00',
                                            '2023-02-01T13:01:00',
                                            '2023-02-01T13:02:00',
                                            '2023-02-01T13:03:00',
                                            '2023-02-01T13:04:00',
                                            '2023-02-01T13:05:00',
                                            '2023-02-01T13:06:00',
                                            '2023-02-01T13:07:00',
                                            '2023-02-01T13:08:00',
                                            '2023-02-01T13:09:00']

    response = await client.get(
        url_path_for(
            get_status.__name__,
            short_url_id='6b990563b16cbe9f07',
        ), params={'full_info': True,
                   'max_result': 3,
                   'offset': 5}
    )
    assert response.status_code == status.HTTP_200_OK
    assert response.json().get('redirects') == 3
    assert response.json().get('times') == ['2023-02-01T13:05:00',
                                            '2023-02-01T13:06:00',
                                            '2023-02-01T13:07:00']

    response = await client.get(
        url_path_for(
            get_status.__name__,
            short_url_id='6b990563b16cbe9f07',
        ), params={'full_info': True,
                   'max_result': 10,
                   'offset': 7}
    )
    assert response.status_code == status.HTTP_200_OK
    assert response.json().get('redirects') == 3
    assert response.json().get('times') == ['2023-02-01T13:07:00',
                                            '2023-02-01T13:08:00',
                                            '2023-02-01T13:09:00']


async def test_get_non_existing_url(
        client: AsyncClient,
        url_path_for: Callable,
        create_url_and_redirects: Callable
) -> None:
    response = await client.get(url_path_for(
        get_status.__name__,
        short_url_id='not_exists'
    ))
    assert response.status_code == status.HTTP_404_NOT_FOUND


async def test_get_deleted_url(client: AsyncClient,
                               url_path_for: Callable,
                               create_url_and_redirects: Callable) -> None:
    response = await client.get(url_path_for(
        get_status.__name__,
        short_url_id='8f7a675f2b54a804e5'
    ))
    assert response.status_code == status.HTTP_404_NOT_FOUND
