from controllers.handlers.base import MessageHandler
from controllers.commands.base import TextCommandHandler
from controllers.commands.explain_command_handler import ExplainCommandHandler
from controllers.commands.learn_command_handler import LearnCommandHandler
from controllers.commands.defalult_command_handler import DefaultCommandHandler
from cache.user_state import get_user_state
from clients.feishu.message import send_text_to_user
from typing import List
import json
from cache.user_state import UserState
from log import logger
from cache.user_state import get_next_question
from agents.learning import check_answer
from cache.question import get_question, get_knowledge_point


class TextMessageHandler(MessageHandler):
    def __init__(self):
        self.command_handlers: List[TextCommandHandler] = [
            ExplainCommandHandler(),
            LearnCommandHandler(),
            DefaultCommandHandler(),  # Default handler should be last
        ]

    def handle(self, open_id: str, content: str) -> None:
        try:
            data = json.loads(content)
            text = data['text']
            
            user_state = get_user_state(open_id)
            if user_state == UserState.LEARNING:
                self._handle_check_learning(open_id, text)
                return

            for handler in self.command_handlers:
                if handler.can_handle(text):
                    handler.handle(open_id, text)
                    break
                    
        except Exception as e:
            logger.exception(f"Error handling text message: {e}")

    def _handle_check_learning(self, open_id: str, text: str) -> None:
        next_question, last_question = get_next_question(open_id)
        if last_question:
            feedback = check_answer(get_question(last_question), get_knowledge_point(last_question), text)
            send_text_to_user(open_id, feedback)
        if next_question:
            send_text_to_user(open_id, next_question)