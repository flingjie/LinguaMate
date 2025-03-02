import feedparser
from ..source_interface import DataSource, News 
import ssl
ssl._create_default_https_context = ssl._create_unverified_context
from log import logger
from utils.date import parse_time_string
from utils.http_utils import fetch_url_content
from agents.news import extract_summary, classify_article


class HackerNewsSource(DataSource):
    def __init__(self):
        super().__init__()
        self.url = 'https://news.ycombinator.com/rss'
        
    def fetch_data(self):
        try:
            feed = feedparser.parse(self.url)
            news = []
            for entry in feed.entries:
                # logger.debug(f"Entry: {entry}") 
                published_at = parse_time_string(entry.get('published', ''))
                link = entry.get('link', '')
                if not link:
                    continue
                title = entry.title
                content = fetch_url_content(link)
                category = classify_article(content)
                logger.debug(f"title: {title}")
                logger.debug(f"category: {category}")
                if category != 'LLM':
                    continue
                summary = extract_summary(content)
                logger.debug(f"link: {link}\n summary:\n {summary}")
                news.append(News(
                    title=title,
                    summary=summary,
                    link=link,
                    category=category,
                    from_source='hacker_news',
                    published_at=published_at
                ))
            return news
        except Exception as e:
            logger.error(f"Error fetching data from {self.url}: {e}")
            return []
