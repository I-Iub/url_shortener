import datetime
import logging
from hashlib import blake2b
from typing import List, Tuple, Union

from sqlalchemy import func
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.sql.expression import select

from core.config import SHORT_URL_LENGTH
from models.urls import Pass, URL

log = logging.getLogger()


async def add_link(original_url: str,
                   session: AsyncSession) -> str:
    path_part = blake2b(digest_size=SHORT_URL_LENGTH)
    path_part.update(original_url.encode())
    shorten_url_id = path_part.hexdigest()

    result = await session.execute(
        select(URL).where(URL.original == original_url)  # noqa
    )
    url: URL = result.scalar()
    if url is None:
        url = URL(original=original_url, short=shorten_url_id)
    pass_ = Pass(url=url, time=datetime.datetime.now())
    session.add(pass_)
    await session.commit()
    return url.short


async def get_original(short_url_id: str,
                       session: AsyncSession) -> Union[str, None]:
    result = await session.execute(
        select(URL.original).where(URL.short == short_url_id)  # noqa
    )
    original_url = result.scalar()
    if original_url is None:
        return
    return original_url


async def get_url_status(
        short_url_id: str,
        session: AsyncSession,
        full_info: bool = False,
        max_result: int = 10,
        offset: int = 0
) -> Tuple[int, Union[List[datetime.datetime], None]]:

    passes = await session.execute(
        select(func.count()).join_from(URL, Pass)
        .where(URL.short == short_url_id)  # noqa
    )
    if not full_info:
        return passes.scalar(), None

    times = await session.execute(
        select(Pass.time).join_from(URL, Pass)
        .where(URL.short == short_url_id)  # noqa
        .limit(max_result).offset(offset)
    )
    return passes.scalar(), list(times.scalars())
