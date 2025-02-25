import lark_oapi as lark
from lark_oapi.api.im.v1 import *
from log import logger
import json
from db import save_dialog, get_recent_dialogs
from agents.chatter import chat
from agents.grammar_checker import is_grammer_right, get_suggestion
from clients.feishu.message import send_text_to_user
import threading


def send_msg_to_user(user_id, msg, msg_type):
    try:
    
        if msg_type == 'text':
            send_text_to_user(user_id, msg)
        elif msg_type == 'image':
            pass
        else:
            logger.warning(f'unsupport type {msg_type}')
    except Exception as e:
        logger.exception(f"fail to send msg: {e}")


def handle_message(open_id, msg_type, content) -> None:
    try:
        if msg_type == 'text':
            data = json.loads(content)
            text = data['text']
            save_dialog(user_id=open_id, content=text, role='user')
        
            if is_grammer_right(text):
                messages = get_recent_dialogs(user_id=open_id)
                response = chat(messages)
                save_dialog(user_id=open_id, content=response, role='assistant')
                send_msg_to_user(open_id, response, 'text')
                logger.debug(f'messages: {messages}')
            else:
                suggestion = get_suggestion(text)
                save_dialog(user_id=open_id, content=suggestion, role='assistant')
                send_msg_to_user(open_id, suggestion, 'text')
            
        else:
            logger.info(f'ignore msg type:{msg_type}')
        
    except Exception as e:
        logger.exception(f"Error handling text message: {e}")


def do_p2_im_message_receive_v1(data: lark.im.v1.P2ImMessageReceiveV1) -> None:
    logger.info(f'[ do_p2_im_message_receive_v1 access ], data: {lark.JSON.marshal(data, indent=2)}')
    try:
        event = data.event
        open_id = event.sender.sender_id.open_id
        msg_type = event.message.message_type
        thread = threading.Thread(target=handle_message, args=(open_id, msg_type, event.message.content))
        thread.start()
    except Exception as e:
        logger.exception(e)