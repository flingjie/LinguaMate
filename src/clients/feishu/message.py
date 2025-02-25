from .base import get_client
from lark_oapi.api.im.v1 import *
import json
import lark_oapi as lark
from log import logger


def send_text_to_user(receive_id, content):
    logger.debug(f'{user_id}, msg: {content}')
    request: CreateMessageRequest = CreateMessageRequest.builder() \
        .request_body(CreateMessageRequestBody.builder()
            .receive_id(receive_id)
            .msg_type("text")
            .content(json.dumps({'text': content}))
            .build()) \
        .receive_id_type('open_id') \
        .build()

    # 发起请求
    client = get_client()
    response: CreateMessageResponse = client.im.v1.message.create(request)

    # 处理失败返回
    if not response.success():
        lark.logger.error(
            f"client.im.v1.message.create failed, code: {response.code}, msg: {response.msg}, log_id: {response.get_log_id()}, resp: \n{json.dumps(json.loads(response.raw.content), indent=4, ensure_ascii=False)}")
        return
    
    lark.logger.info(lark.JSON.marshal(response.data, indent=4))
    return

if __name__ == "__main__":
    receiver_id = 'ou_f5804cb29e2f965b76528499d80b089e'
    content = 'hi'
    send_text_to_user(receiver_id, content)