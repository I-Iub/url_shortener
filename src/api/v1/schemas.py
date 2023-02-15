import datetime
from typing import List
from pydantic import AnyUrl, BaseModel, HttpUrl


class OriginalURL(BaseModel):
    url: AnyUrl


class ShortURL(BaseModel):
    short_url_id: str


class Status(BaseModel):
    passes: int
    times: List[datetime.datetime] = None
