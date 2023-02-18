import os
from logging import config as logging_config

from core.logger import LOGGING

logging_config.dictConfig(LOGGING)

PROJECT_NAME = os.getenv('PROJECT_NAME', 'url shortener')
PROJECT_HOST = os.getenv('PROJECT_HOST', '127.0.0.1')
PROJECT_PORT = int(os.getenv('PROJECT_PORT', '8080'))

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
BLACK_LIST = {'42.42.42.42'}
SOURCE_NETLOCK = 'https://shortener.url'
SHORT_URL_LENGTH = 9
