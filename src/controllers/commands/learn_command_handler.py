from .base import TextCommandHandler
from cache.user_state import init_questions, get_next_question
from utils.http_utils import fetch_url_content
from clients.feishu.message import send_text_to_user
from agents.learning import generate_questions
from log import logger

class LearnCommandHandler(TextCommandHandler):
    def can_handle(self, text: str) -> bool:
        return text.startswith('learn')

    def handle(self, open_id: str, text: str) -> None:
        url = text.split(' ')[1]
        content = fetch_url_content(url)
        questions = generate_questions(content)
        # logger.debug(questions)
        question = init_questions(open_id, content, questions)
        send_text_to_user(open_id, question)