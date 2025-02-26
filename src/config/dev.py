import os
from enum import Enum

from dotenv import load_dotenv
load_dotenv()

APP_ID = os.getenv('FEISHU_APP_ID')
APP_SECRET = os.getenv('FEISHU_APP_SECRET')
APP_VERIFICATION_TOKEN = os.getenv('FEISHU_APP_SECRET')
APP_ENCRYPT_KEY = os.getenv('FEISHU_APP_VERIFICATION_TOKEN')


LOG_PATH = '../log'


API_BASE = 'http://localhost:11434'

MONGO_URL = 'mongodb://localhost:27017/'
MONGO_DB_NAME = 'lucy'
MONGO_DIALOG_COL_NAME = 'dialog'
MONGO_NEWS_COL_NAME = 'news'


class ModelName(Enum):
    DEEPSEEK = 'ollama/deepseek-r1:14b'
    QWEN = 'ollama/qwen2.5:7b'
