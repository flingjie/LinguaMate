import lark_oapi as lark
from lark_oapi.api.im.v1 import *
from log import logger
import json
from storage import save_dialog, get_recent_dialogs
from agents.chatter import get_chat_response
from agents.grammar import is_grammar_correct, get_grammar_suggestions
from agents.word_hint import get_word_hint, get_word_meaning
from clients.feishu.message import send_text_to_user, send_image_to_user
import threading
from utils.sd import generate_image
import os
from config.dev import IMAGE_OUTPUT_DIR


def get_image_from_cache(word):
    filepath = os.path.join(IMAGE_OUTPUT_DIR, f"{word}.png")
    if os.path.exists(filepath):
        return filepath
    return None

def handle_hint_message(open_id, text):
    word = text.split(' ')[1]
    meaning = get_word_meaning(word)
    send_text_to_user(open_id, meaning)
    # logger.info(f'hint: {hint}')
    filepath = get_image_from_cache(word)
    if not filepath:
        hint = get_word_hint(word, meaning)
        filepath = generate_image(word, hint)
    send_image_to_user(open_id, filepath)



def handle_message(open_id, msg_type, content) -> None:
    try:
        if msg_type == 'text':
            data = json.loads(content)
            text = data['text']
            
            if text.startswith('explain'):
                handle_hint_message(open_id, text)
                return
            
            if is_grammar_correct(text):
                history = get_recent_dialogs(user_id=open_id)
                save_dialog(user_id=open_id, content=text, role='user')
                response = get_chat_response(text, history)
                save_dialog(user_id=open_id, content=response, role='assistant')
                send_text_to_user(open_id, response, 'text')
                # logger.debug(f'messages: {messages}')
            else:
                suggestions = get_grammar_suggestions(text)
                save_dialog(user_id=open_id, content=text, role='user')
                save_dialog(user_id=open_id, content=suggestions, role='assistant')
                send_text_to_user(open_id, suggestions, 'text')
            
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