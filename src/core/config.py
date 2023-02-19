import os
from logging import config as logging_config

from dotenv import load_dotenv

from src.core.logger import LOGGING

logging_config.dictConfig(LOGGING)
load_dotenv()

PROJECT_NAME = os.getenv('PROJECT_NAME', 'url shortener')
PROJECT_HOST = os.getenv('PROJECT_HOST', '127.0.0.1')
PROJECT_PORT = int(os.getenv('PROJECT_PORT', '8080'))

DSN = os.getenv(
    'DSN', 'postgresql+asyncpg://postgres:postgres@localhost:5432/urls'
)
_black_list = os.getenv('BLACK_LIST')
BLACK_LIST = (set() if _black_list is None
              else set(ip.strip() for ip in _black_list.split(';')))
SOURCE_NETLOCK = os.getenv('SOURCE_NETLOCK', 'https://shortener.url')
SHORT_URL_LENGTH = int(os.getenv('SHORT_URL_LENGTH', 9))
