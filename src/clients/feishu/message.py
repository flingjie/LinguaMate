from .base import client
from lark_oapi.api.im.v1 import *
import json
import lark_oapi as lark
from log import logger
import os


def send_text_to_user(receive_id, content):
    logger.debug(f'{receive_id}, msg: {content}')
    request: CreateMessageRequest = CreateMessageRequest.builder() \
        .request_body(CreateMessageRequestBody.builder()
            .receive_id(receive_id)
            .msg_type("text")
            .content(json.dumps({'text': content}))
            .build()) \
        .receive_id_type('open_id') \
        .build()

    # 发起请求
    response: CreateMessageResponse = client.im.v1.message.create(request)

    # 处理失败返回
    if not response.success():
        lark.logger.error(
            f"client.im.v1.message.create failed, code: {response.code}, msg: {response.msg}, log_id: {response.get_log_id()}, resp: \n{json.dumps(json.loads(response.raw.content), indent=4, ensure_ascii=False)}")
        return
    
    lark.logger.info(lark.JSON.marshal(response.data, indent=4))
    return

def send_image_to_user(receive_id, filepath):
    create_image_req = CreateImageRequest.builder() \
        .request_body(CreateImageRequestBody.builder()
                      .image_type("message")
                      .image(open(filepath, 'rb'))
                      .build()) \
        .build()

    create_image_resp = client.im.v1.image.create(create_image_req)

    if not create_image_resp.success():
        lark.logger.error(
            f"client.im.v1.image.create failed, "
            f"code: {create_image_resp.code}, "
            f"msg: {create_image_resp.msg}, "
            f"log_id: {create_image_resp.get_log_id()}")
        return create_image_resp

    # 发送消息
    option = lark.RequestOption.builder().headers({"X-Tt-Logid": create_image_resp.get_log_id()}).build()
    create_message_req = CreateMessageRequest.builder() \
        .receive_id_type('open_id') \
        .request_body(CreateMessageRequestBody.builder()
                      .receive_id(receive_id)
                      .msg_type("image")
                      .content(json.dumps({'image_key': create_image_resp.data.image_key}))
                      .build()) \
        .build()

    create_message_resp: CreateMessageResponse = client.im.v1.message.create(create_message_req, option)

    if not create_message_resp.success():
        lark.logger.error(
            f"client.im.v1.message.create failed, "
            f"code: {create_message_resp.code}, "
            f"msg: {create_message_resp.msg}, "
            f"log_id: {create_message_resp.get_log_id()}")
        return create_message_resp
    lark.logger.info(lark.JSON.marshal(create_message_resp.data, indent=4))


def upload_file(filepath, duration, file_type):
    request: CreateFileRequest = CreateFileRequest.builder() \
        .request_body(CreateFileRequestBody.builder()
            .file_type(file_type)
            .file_name(os.path.basename(filepath))
            .file(open(filepath, 'rb'))
            .duration(duration)
            .build()) \
        .build()

    # 发起请求
    response: CreateFileResponse = client.im.v1.file.create(request)

    # 处理失败返回
    if not response.success():
        lark.logger.error(
            f"client.im.v1.file.create failed, code: {response.code}, msg: {response.msg}, log_id: {response.get_log_id()}, resp: \n{json.dumps(json.loads(response.raw.content), indent=4, ensure_ascii=False)}")
        return ""

    # 处理业务结果
    lark.logger.info(lark.JSON.marshal(response.data, indent=4))
    file_key = response.data.file_key
    logger.debug(f'file_key: {file_key}')
    return file_key

def send_audio_to_user(receive_id, filepath, duration):
    logger.debug(f'{receive_id}, filepath: {filepath}, duration: {duration}')
    
    file_key = upload_file(filepath, duration, 'opus')
    if not file_key:
        logger.error(f'upload_file failed, filepath: {filepath}, duration: {duration}')
        return

    create_message_req = CreateMessageRequest.builder() \
        .receive_id_type('open_id') \
        .request_body(CreateMessageRequestBody.builder()
                      .receive_id(receive_id)
                      .msg_type("audio")
                      .content(json.dumps({'file_key': file_key}))
                      .build()) \
        .build()

    create_message_resp: CreateMessageResponse = client.im.v1.message.create(create_message_req)

    if not create_message_resp.success():
        lark.logger.error(
            f"client.im.v1.message.create failed, "
            f"code: {create_message_resp.code}, "
            f"msg: {create_message_resp.msg}, "
            f"log_id: {create_message_resp.get_log_id()}")
        return create_message_resp
    lark.logger.info(lark.JSON.marshal(create_message_resp.data, indent=4))


if __name__ == "__main__":
    receiver_id = 'ou_f5804cb29e2f965b76528499d80b089e'
    # content = 'hi'
    # send_text_to_user(receiver_id, content)
    # filepath = '../output/audio/2025-02-26-20-20-07.opus'
    # duration = 2922
    # send_audio_to_user(receiver_id, filepath, duration)
    filepath = '../output/image/robot1.jpeg'
    send_image_to_user(receiver_id, filepath)