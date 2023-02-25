import datetime
from hashlib import blake2b
from typing import List, Optional, Tuple, Union

from sqlalchemy.dialects.postgresql import insert
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.sql.expression import select, update

from src.core.config import SHORT_URL_LENGTH
from src.models.urls import URL, Pass


def get_shorten_url_id(original_url: str) -> str:
    path_part = blake2b(digest_size=SHORT_URL_LENGTH)
    path_part.update(original_url.encode())
    return path_part.hexdigest()


async def create_records(original_url: str,
                         session: AsyncSession) -> str:
    shorten_url_id = get_shorten_url_id(original_url)
    url_record = [dict(original=original_url, short=shorten_url_id)]
    statement = (
        insert(URL).values(url_record)
        .on_conflict_do_update(index_elements=['original'],
                               set_={'deleted': False})
        .returning(URL.id)
    )
    result = await session.execute(statement)
    url_id = result.scalar()
    pass_ = Pass(url_id=url_id, time=datetime.datetime.now())
    session.add(pass_)
    await session.commit()
    return shorten_url_id


async def add_url_batch(original_urls: List[str],
                        session: AsyncSession) -> List[str]:
    shorten_urls = list(map(get_shorten_url_id, original_urls))
    unique_pairs = set(zip(original_urls, shorten_urls))
    values = [{'original': original, 'short': short}
              for original, short in unique_pairs]
    statement = (
        insert(URL).values(values)
        .on_conflict_do_update(index_elements=['original'],
                               set_={'deleted': False})
    )
    await session.execute(statement)
    await session.commit()
    return shorten_urls


async def mark_as_deleted(url: str, session: AsyncSession) -> bool:
    statement = (
        update(URL).where(URL.original == url).values(deleted=True)
        .returning(URL.id)
    )
    result = await session.execute(statement)
    if result.scalar() is None:
        return False
    await session.commit()
    return True


async def get_original(short_url_id: str,
                       session: AsyncSession) -> Union[str, bool, None]:
    result = await session.execute(
        select(URL).where(URL.short == short_url_id)
    )
    original_url = result.scalar()
    if original_url is None:
        return
    if original_url.deleted:
        return False
    return original_url.original


async def get_url_status(
        short_url_id: str,
        session: AsyncSession,
        full_info: bool = False,
        max_result: int = 10,
        offset: int = 0
) -> Tuple[int, Optional[List[datetime.datetime]]]:
    result = await session.execute(
        select(Pass.time).join_from(URL, Pass)
        .where(URL.short == short_url_id).where(URL.deleted == False)
        .limit(max_result).offset(offset)
    )
    times = list(result.scalars())
    if not full_info:
        return len(times), None
    return len(times), times
