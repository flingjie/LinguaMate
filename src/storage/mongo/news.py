from datetime import datetime, timedelta
from config import MONGO_NEWS_COL_NAME
from .base import db


news_col = db[MONGO_NEWS_COL_NAME]


def save_dialog(title: str,
                content: str,
                author: str,
                summary: str,
                link: str,
                from_source: str,
                tags: list=[]
                ):
    doc = {
        'title': title,
        'content': content,
        'author': author,
        'summary': summary,
        'link': link,
        'from_source': from_source,
        'tags': tags,
        'time': datetime.now()
    }
    return news_col.insert_one(doc)