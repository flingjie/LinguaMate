from enum import Enum


class UserState(Enum):
    CHAT = 'chat'
    CHECK_LEARNING = 'check_learning'

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
    _USER_CONTEXT[user_id]['questions'] = questions


def set_cur_question(user_id, question):
    _USER_CONTEXT[user_id]['cur_question'] = question

def get_cur_question(user_id):
    if 'cur_question' not in _USER_CONTEXT[user_id]:
        return ''
    return _USER_CONTEXT[user_id]['cur_question']

def get_next_question(user_id):
    state = get_user_state(user_id)
    if state != UserState.CHECK_LEARNING:
        return ''
    if 'questions' not in _USER_CONTEXT[user_id]:
        return ''
    next_question = _USER_CONTEXT[user_id]['questions'].pop(0)
    set_cur_question(user_id, next_question)
    content = _USER_CONTEXT[user_id]['content']
    return next_question, content

