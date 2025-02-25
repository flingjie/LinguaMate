from datetime import datetime, timedelta
from config import MONGO_DIALOG_COL_NAME
from .base import db


dialog_col = db[MONGO_DIALOG_COL_NAME]


def save_dialog(user_id: str,
                content: str,
                role: str,
                msg_type: str='text'):
    doc = {
        'user_id': user_id,
        'role': role,
        'content': content,
        'msg_type': msg_type,
        'time': datetime.now()
    }
    return dialog_col.insert_one(doc)


def get_recent_dialogs(user_id: str, limit: int = 6):
    ten_mins_ago = datetime.now() - timedelta(minutes=10)
    dialogs = dialog_col.find({
        "user_id": user_id,
        "time": {"$gte": ten_mins_ago}
    }).sort("time", -1).limit(limit)
    messages = []
    for item in dialogs:
        messages.append({
            'role': item['role'],
            'content': item['content']
        })
    return messages