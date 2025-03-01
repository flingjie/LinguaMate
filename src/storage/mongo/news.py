from config import MONGO_NEWS_COL_NAME
from .base import db
from crawl.data_sources.source_interface import News

news_col = db[MONGO_NEWS_COL_NAME]


def save_news(news: News):
    doc = news.to_dict()
    return news_col.insert_one(doc)
