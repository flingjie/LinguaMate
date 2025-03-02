from .base import TextCommandHandler
from cache.image import get_image_from_cache
from agents.word_hint import get_word_hint, get_word_meaning
from clients.feishu.message import send_text_to_user, send_image_to_user
from utils.sd import generate_image


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