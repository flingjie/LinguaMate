from .base import TextCommandHandler
from cache.user_state import init_questions, get_next_question
from utils.http_utils import fetch_url_content
from clients.feishu.message import send_text_to_user

class LearnCommandHandler(TextCommandHandler):
    def can_handle(self, text: str) -> bool:
        return text.startswith('learn')

    def handle(self, open_id: str, text: str) -> None:
        url = text.split(' ')[1]
        content = fetch_url_content(url)
        questions = []
        init_questions(open_id, content, questions)
        next_question, _ = get_next_question(open_id)
        send_text_to_user(open_id, next_question)