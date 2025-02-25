from llm.chat import chat_with_llm
from log import logger


def chat(messages):
    logger.debug(f'messages: {messages}')
    return chat_with_llm(messages)



