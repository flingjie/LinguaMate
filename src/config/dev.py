import os

from dotenv import load_dotenv
load_dotenv()

APP_ID = os.getenv('FEISHU_APP_ID')
APP_SECRET = os.getenv('FEISHU_APP_SECRET')
APP_VERIFICATION_TOKEN = os.getenv('FEISHU_APP_SECRET')
APP_ENCRYPT_KEY = os.getenv('FEISHU_APP_VERIFICATION_TOKEN')


LOG_PATH = '../log'

MODEL_NAME = 'ollama/deepseek-r1:7b'
API_BASE = 'http://localhost:11434'