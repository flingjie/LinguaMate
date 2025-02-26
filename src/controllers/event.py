import lark_oapi as lark
from lark_oapi.api.im.v1 import *
from log import logger
import json
from storage import save_dialog, get_recent_dialogs
from agents.chatter import get_chat_respose
from agents.grammar_checker import is_grammer_right, get_suggestion
from agents.word_hint import get_word_hint
from clients.feishu.message import send_text_to_user, send_image_to_user
import threading
from utils.sd import generate_image


def handle_hint_message(open_id, text):
    word = text.split(' ')[1]
    hint = get_word_hint(word)
    send_text_to_user(open_id, hint)
    # logger.info(f'hint: {hint}')
    filepath = generate_image(hint)
    send_image_to_user(open_id, filepath)



def handle_message(open_id, msg_type, content) -> None:
    try:
        if msg_type == 'text':
            data = json.loads(content)
            text = data['text']
            
            if text.startswith('explain'):
                handle_hint_message(open_id, text)
                return
            
            if is_grammer_right(text):
                history = get_recent_dialogs(user_id=open_id)
                save_dialog(user_id=open_id, content=text, role='user')
                response = get_chat_respose(text, history)
                save_dialog(user_id=open_id, content=response, role='assistant')
                send_text_to_user(open_id, response, 'text')
                # logger.debug(f'messages: {messages}')
            else:
                suggestion = get_suggestion(text)
                save_dialog(user_id=open_id, content=text, role='user')
                save_dialog(user_id=open_id, content=suggestion, role='assistant')
                send_text_to_user(open_id, suggestion, 'text')
            
        else:
            logger.info(f'ignore msg type:{msg_type}')
        
    except Exception as e:
        logger.exception(f"Error handling text message: {e}")


def do_p2_im_message_receive_v1(data: lark.im.v1.P2ImMessageReceiveV1) -> None:
    # logger.info(f'[ do_p2_im_message_receive_v1 access ], data: {lark.JSON.marshal(data, indent=2)}')
    try:
        event = data.event
        open_id = event.sender.sender_id.open_id
        msg_type = event.message.message_type
        thread = threading.Thread(target=handle_message, args=(open_id, msg_type, event.message.content))
        thread.start()
    except Exception as e:
        logger.exception(e)