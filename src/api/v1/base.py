from typing import List, Union

from fastapi import APIRouter, Depends, Response, status

from api.v1.schemas import OriginalURL, ShortURL, ShortURLBatch, Status
from core.config import SOURCE_NETLOCK
from db.database import get_session
from services.base import (add_url, add_url_batch, get_original,
                           get_url_status, mark_as_deleted)

router = APIRouter()


@router.post('/',
             status_code=status.HTTP_201_CREATED,
             summary='Получить сокращённый вариант переданного URL.',
             description='Метод принимает в теле запроса строку URL для '
                         'сокращения и возвращает ответ с кодом 201.')
async def post_url(original_url: OriginalURL,
                   session=Depends(get_session)) -> Union[ShortURL, Response]:
    short_url = await add_url(original_url.url, session)
    return ShortURL(short_url_id=short_url)


@router.post('/shorten',
             status_code=status.HTTP_201_CREATED,
             summary='Получить сокращённые URL для списка URL.',
             description='Метод принимает в теле запроса список строк URL для '
                         'сокращения и возвращает сокращённые URL.')
async def post_many_url(original_urls: List[OriginalURL],
                        session=Depends(get_session)):
    original = [model.url for model in original_urls]
    short_url_ids = await add_url_batch(original, session)
    return [
        ShortURLBatch(
            short_url_id=url_id,
            short_url=SOURCE_NETLOCK + url_id
        ) for url_id in short_url_ids
    ]


@router.delete('/delete',
               status_code=status.HTTP_204_NO_CONTENT,
               summary='Пометить переданную url-ссылку как удалённую.')
async def delete_url(original_url: OriginalURL,
                     session=Depends(get_session)):
    deleted = await mark_as_deleted(original_url.url, session)
    if not deleted:
        return Response(status_code=status.HTTP_404_NOT_FOUND)


@router.get('/{short_url_id}',
            status_code=status.HTTP_307_TEMPORARY_REDIRECT,
            summary='Возвращает оригинальный URL.',
            description='Метод принимает в качестве параметра идентификатор '
                        'сокращённого URL и возвращает ответ с кодом 307 и '
                        'оригинальным URL в заголовке Location.')
async def get_original_url(
        short_url_id, session=Depends(get_session)
) -> Union[OriginalURL, Response]:
    original_url = await get_original(short_url_id, session)
    if original_url is None:
        return Response(status_code=status.HTTP_404_NOT_FOUND)
    if original_url is False:
        return Response(status_code=status.HTTP_410_GONE)
    return OriginalURL(url=original_url)


@router.get('/{short_url_id}/status',
            summary='Возвращает статус использования URL.',
            description='Метод принимает в качестве параметра идентификатор '
                        'сокращённого URL и возвращает информацию о '
                        'количестве переходов, совершенных по ссылке.')
async def get_status(short_url_id,
                     session=Depends(get_session),
                     full_info=False,
                     max_result=10,
                     offset=0) -> Union[Status, Response]:
    passes, times = await get_url_status(
        short_url_id, session, full_info, max_result, offset
    )
    if not passes:
        return Response(status_code=status.HTTP_404_NOT_FOUND)
    return Status(passes=passes, times=times)
