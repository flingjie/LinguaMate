from controllers.handlers.base import MessageHandler
from clients.feishu.message import get_message_by_id, reply_audio_to_message
from log import logger
import json
from utils.tts import text2audio


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