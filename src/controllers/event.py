import lark_oapi as lark
from log import logger
import json
from db import save_dialog, get_recent_dialogs
from agents.chatter import chat
from agents.grammar_checker import check_grammar


def send_msg_to_user(user_id, msg, msg_type):
    pass


def do_p2_im_message_receive_v1(data: lark.im.v1.P2ImMessageReceiveV1) -> None:
    # logger.info(f'[ do_p2_im_message_receive_v1 access ], data: {lark.JSON.marshal(data, indent=2)}')
    try:
        event = data.event
        union_id = event.sender.sender_id.union_id
        msg_type = event.message.message_type
        if msg_type == 'text':
            content = json.loads(event.message.content)
            text = content['text']
            save_dialog(user_id=union_id, content=text, role='user')

            mistake = check_grammar(text)
            if mistake:
                save_dialog(user_id=union_id, content=mistake, role='assistant')
            else:
                messages = get_recent_dialogs(user_id=union_id)
                response = chat(messages)
                save_dialog(user_id=union_id, content=response, role='assistant')
            logger.debug(f'messages: {messages}')
        else:
            logger.info(f'ignore msg type:{msg_type}')
    except Exception as e:
        logger.exception(e)