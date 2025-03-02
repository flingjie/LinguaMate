from .base import TextCommandHandler
from clients.feishu.message import send_text_to_user
from agents.grammar import is_grammar_correct, get_grammar_suggestions
from agents.chatter import get_chat_response
from storage import get_recent_dialogs, save_dialog


class DefaultCommandHandler(TextCommandHandler):
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