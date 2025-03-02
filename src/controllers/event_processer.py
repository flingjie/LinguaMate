import lark_oapi as lark
from lark_oapi.api.im.v1 import *
from log import logger
import threading
from typing import Dict
from controllers.handlers.base import MessageHandler, MessageType
from controllers.handlers.text_message_handler import TextMessageHandler
from controllers.handlers.reaction_handler import ReactionMessageHandler


class MessageProcessor:
    def __init__(self):
        self.handlers: Dict[MessageType, MessageHandler] = {
            MessageType.TEXT: TextMessageHandler(),
            MessageType.REACTION: ReactionMessageHandler(),
        }

    def process_message(self, message_type: MessageType, open_id: str, content: str) -> None:
        handler = self.handlers.get(message_type)
        if handler:
            thread = threading.Thread(target=handler.handle, args=(open_id, content))
            thread.start()
        else:
            logger.info(f'ignore msg type:{message_type}')

def do_p2_im_message_receive_v1(data: lark.im.v1.P2ImMessageReceiveV1) -> None:
    try:
        event = data.event
        processor = MessageProcessor()
        processor.process_message(
            MessageType(event.message.message_type),
            event.sender.sender_id.open_id,
            event.message.content
        )
    except Exception as e:
        logger.exception(e)

def do_p2_im_message_reaction_v1(data: lark.im.v1.P2ImMessageReactionCreatedV1) -> None:
    try:
        event = data.event
        processor = MessageProcessor()
        processor.process_message(
            MessageType.REACTION,
            event.user_id.open_id,
            event.message_id
        )
    except Exception as e:
        logger.exception(e)