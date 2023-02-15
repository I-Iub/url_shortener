from sqlalchemy import Column, DateTime, ForeignKey, Integer, String
from sqlalchemy.orm import relationship

from db.database import Base


class URL(Base):
    __tablename__ = 'urls'

    id = Column(Integer, primary_key=True, index=True)
    original = Column(String, unique=True, index=True)
    short = Column(String, unique=True, index=True)


class Pass(Base):
    __tablename__ = 'passes'

    id = Column(Integer, primary_key=True, index=True)
    url_id = Column(Integer,
                    ForeignKey('urls.id', ondelete='CASCADE'),
                    nullable=False)
    url = relationship(URL, backref='passes')
    time = Column(DateTime)
