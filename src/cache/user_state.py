from enum import Enum
from cache.question import get_question, get_knowledge_point

class UserState(Enum):
    CHAT = 'chat'
    LEARNING = 'learning'

_USER_CONTEXT = {}


def get_user_state(user_id):
    if user_id not in _USER_CONTEXT:
        _USER_CONTEXT[user_id] = {'state': UserState.CHAT}
    return _USER_CONTEXT[user_id].get('state', UserState.CHAT)

def set_user_state(user_id, state):
    _USER_CONTEXT[user_id] = {'state': state}


def init_questions(user_id, content, questions):
    if user_id not in _USER_CONTEXT:
        _USER_CONTEXT[user_id] = {'state': UserState.CHAT}
    _USER_CONTEXT[user_id]['content'] = content
    current_question = questions.pop(0)
    _USER_CONTEXT[user_id]['questions'] = questions
    _USER_CONTEXT[user_id]['current_question'] = current_question
    _USER_CONTEXT[user_id]['state'] = UserState.LEARNING
    return get_question(current_question)


def set_current_question(user_id, question):
    _USER_CONTEXT[user_id]['current_question'] = question

def get_current_question(user_id):
    if 'current_question' not in _USER_CONTEXT[user_id]:
        return ''
    return _USER_CONTEXT[user_id]['current_question']

def get_next_question(user_id):
    state = get_user_state(user_id)
    if state != UserState.LEARNING:
        return '', {}
    if 'questions' not in _USER_CONTEXT[user_id]:
        return '', {}
    last_question = _USER_CONTEXT[user_id].get('current_question', {})
    questions = _USER_CONTEXT[user_id]['questions']
    if not questions:
        _USER_CONTEXT[user_id]['state'] = UserState.CHAT
        return '', last_question
    next_question = questions.pop(0)
    set_current_question(user_id, next_question)
    return get_question(next_question), last_question

