import os
from enum import Enum

from dotenv import load_dotenv
load_dotenv()

APP_ID = os.getenv('FEISHU_APP_ID')
APP_SECRET = os.getenv('FEISHU_APP_SECRET')
APP_VERIFICATION_TOKEN = os.getenv('FEISHU_APP_SECRET')
APP_ENCRYPT_KEY = os.getenv('FEISHU_APP_VERIFICATION_TOKEN')


LOG_PATH = '../log'




MONGO_URL = 'mongodb://localhost:27017/'
MONGO_DB_NAME = 'lucy'
MONGO_DIALOG_COL_NAME = 'dialog'
MONGO_NEWS_COL_NAME = 'news'

OUTPUT_DIR = "../output"
IMAGE_OUTPUT_DIR = os.path.join(OUTPUT_DIR, "image")


class ModelName(Enum):
    DEEPSEEK7B = 'ollama/deepseek-r1:7b'
    DEEPSEEK14B = 'ollama/deepseek-r1:14b'
    QWEN = 'ollama/qwen2.5:7b'
    ARK_DEEPSEEKV3 = 'volcengine/deepseek-v3-241226'


API_BASE_MAP = {
    ModelName.DEEPSEEK7B: 'http://localhost:11434',
    ModelName.DEEPSEEK14B: 'http://localhost:11434',
    ModelName.QWEN: 'http://localhost:11434',
    ModelName.ARK_DEEPSEEKV3: 'https://ark.cn-beijing.volces.com/api/v3',
}