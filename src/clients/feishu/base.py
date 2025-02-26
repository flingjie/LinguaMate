import lark_oapi as lark
from config import APP_ID, APP_SECRET

def get_client():
    client = lark.Client.builder() \
        .app_id(APP_ID) \
        .app_secret(APP_SECRET) \
        .log_level(lark.LogLevel.INFO) \
        .build()
    return client

client = get_client()