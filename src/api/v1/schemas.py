import datetime
from typing import List

from pydantic import AnyUrl, BaseModel


class OriginalURL(BaseModel):
    url: AnyUrl


class ShortURL(BaseModel):
    short_url_id: str


class ShortURLBatch(BaseModel):
    short_url_id: str
    short_url: str


class Status(BaseModel):
    redirects: int
    times: List[datetime.datetime] = None
