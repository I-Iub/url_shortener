from sqlalchemy import Boolean, Column, DateTime, ForeignKey, Integer, String
from sqlalchemy.orm import relationship

from src.db.database import Base

MAX_LEN_ORIGINAL = 2048
MAX_LEN_SHORT = 100


class URL(Base):
    __tablename__ = 'urls'

    id = Column(Integer, primary_key=True, index=True)
    original = Column(String(length=MAX_LEN_ORIGINAL), unique=True, index=True)
    short = Column(String(length=MAX_LEN_SHORT), unique=True, index=True)
    deleted = Column(Boolean, default=False)


class Redirects(Base):
    __tablename__ = 'redirects'

    id = Column(Integer, primary_key=True, index=True)
    url_id = Column(Integer,
                    ForeignKey('urls.id', ondelete='CASCADE'),
                    nullable=False)
    url = relationship(URL, backref='redirects')
    time = Column(DateTime)
