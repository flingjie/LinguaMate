from crawl.db_observer import DBObserver
from crawl.data_sources.rss.hacker_news import HackerNewsSource
from crawl.data_collector import DataCollector

def run_crawl():
    db_observer = DBObserver()
    hacker_news_source = HackerNewsSource()
    
    collector = DataCollector()
    collector.add_data_source(hacker_news_source)
    collector.add_observer(db_observer)
    collector.fetch_data()

if __name__ == "__main__":
    run_crawl()