from typing import Union
from fastapi import APIRouter, Depends, HTTPException, Response, status

from api.v1.schemas import OriginalURL, ShortURL, Status
from db.database import get_session
from services.base import add_link, get_original, get_url_status

router = APIRouter()


@router.post('/',
             status_code=status.HTTP_201_CREATED,
             summary='Получить сокращённый вариант переданного URL.',
             description='Метод принимает в теле запроса строку URL для '
                         'сокращения и возвращает ответ с кодом 201.')
async def post_url(original_url: OriginalURL,
                   session=Depends(get_session)) -> Union[ShortURL, Response]:
    short_url = await add_link(original_url.url, session)
    return ShortURL(short_url_id=short_url)


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
