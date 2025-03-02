import lark_oapi as lark
from lark_oapi.api.im.v1 import *
from log import logger
import json
from storage import save_dialog, get_recent_dialogs
from agents.chatter import get_chat_response
from agents.grammar import is_grammar_correct, get_grammar_suggestions
from agents.word_hint import get_word_hint, get_word_meaning
from clients.feishu.message import send_text_to_user, send_image_to_user, get_message_by_id, reply_audio_to_message
from utils.tts import text2audio
import threading
from utils.sd import generate_image
import os
from config.dev import IMAGE_OUTPUT_DIR
from cache.user_state import init_check_learning, get_next_question, get_user_state, UserState
from utils.http_utils import fetch_url_content
from abc import ABC, abstractmethod
from enum import Enum
from typing import List, Optional, Dict

def get_image_from_cache(word):
    filepath = os.path.join(IMAGE_OUTPUT_DIR, f"{word}.png")
    if os.path.exists(filepath):
        return filepath
    return None

class MessageType(Enum):
    TEXT = "text"
    REACTION = "reaction"

class MessageHandler(ABC):
    @abstractmethod
    def handle(self, open_id: str, content: str) -> None:
        pass

class TextCommandHandler(ABC):
    @abstractmethod
    def can_handle(self, text: str) -> bool:
        pass

    @abstractmethod
    def handle(self, open_id: str, text: str) -> None:
        pass

class ExplainCommandHandler(TextCommandHandler):
    def can_handle(self, text: str) -> bool:
        return text.startswith('explain')

    def handle(self, open_id: str, text: str) -> None:
        word = text.split(' ')[1]
        meaning = get_word_meaning(word)
        send_text_to_user(open_id, meaning)
        
        filepath = get_image_from_cache(word)
        if not filepath:
            hint = get_word_hint(word, meaning)
            filepath = generate_image(word, hint)
        send_image_to_user(open_id, filepath)

class LearnCommandHandler(TextCommandHandler):
    def can_handle(self, text: str) -> bool:
        return text.startswith('learn')

    def handle(self, open_id: str, text: str) -> None:
        url = text.split(' ')[1]
        content = fetch_url_content(url)
        questions = []
        init_check_learning(open_id, content, questions)

class ChatMessageHandler(TextCommandHandler):
    def can_handle(self, text: str) -> bool:
        return True  # Default handler for regular chat messages

    def handle(self, open_id: str, text: str) -> None:
        if is_grammar_correct(text):
            history = get_recent_dialogs(user_id=open_id)
            save_dialog(user_id=open_id, content=text, role='user')
            response = get_chat_response(text, history)
            save_dialog(user_id=open_id, content=response, role='assistant')
            send_text_to_user(open_id, response, 'text')
        else:
            suggestions = get_grammar_suggestions(text)
            save_dialog(user_id=open_id, content=text, role='user')
            save_dialog(user_id=open_id, content=suggestions, role='assistant')
            send_text_to_user(open_id, suggestions, 'text')

class TextMessageHandler(MessageHandler):
    def __init__(self):
        self.command_handlers: List[TextCommandHandler] = [
            ExplainCommandHandler(),
            LearnCommandHandler(),
            ChatMessageHandler(),  # Default handler should be last
        ]

    def handle(self, open_id: str, content: str) -> None:
        try:
            data = json.loads(content)
            text = data['text']
            
            user_state = get_user_state(open_id)
            if user_state == UserState.CHECK_LEARNING:
                self._handle_check_learning(open_id, text)
                return

            for handler in self.command_handlers:
                if handler.can_handle(text):
                    handler.handle(open_id, text)
                    break
                    
        except Exception as e:
            logger.exception(f"Error handling text message: {e}")

    def _handle_check_learning(self, open_id: str, text: str) -> None:
        next_question, content = get_next_question(open_id)
        if not next_question:
            send_text_to_user(open_id, '没有更多问题了')
            return
        send_text_to_user(open_id, next_question)

class ReactionMessageHandler(MessageHandler):
    def handle(self, open_id: str, message_id: str) -> None:
        try:
            message = get_message_by_id(message_id)
            for item in message.items:
                if item.msg_type == 'text':
                    body = json.loads(item.body.content)
                    text = body['text']
                    audio_path, duration = text2audio(text)
                    reply_audio_to_message(message_id, audio_path, duration)
                else:
                    logger.info(f'ignore item type:{item.msg_type}')
        except Exception as e:
            logger.exception(e)

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