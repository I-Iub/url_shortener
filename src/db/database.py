import os

from dotenv import load_dotenv
from sqlalchemy import create_engine
from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from typing import AsyncGenerator

load_dotenv('core/.env')

# engine = create_engine(os.environ['SQLALCHEMY_DATABASE_URL'], echo=True)  # todo: удалить echo=True
# SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
# async_session = sessionmaker(
#     engine, class_=AsyncSession, expire_on_commit=False
# )
# Base = declarative_base()

engine = create_async_engine(os.environ['SQLALCHEMY_DATABASE_URL'], echo=True)  # todo: удалить echo=True
async_session = sessionmaker(
    engine, class_=AsyncSession, expire_on_commit=False
)
Base = declarative_base()


async def get_session() -> AsyncGenerator[AsyncSession, None]:
    async with async_session() as session:
        yield session
