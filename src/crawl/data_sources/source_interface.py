from abc import ABC, abstractmethod
from dataclasses import dataclass
from datetime import datetime
from typing import List

@dataclass
class News:
    title: str
    summary: str
    link: str
    from_source: str
    category: str
    tags: List[str] = None
    published_at: datetime = None
    created_at: datetime = None

    def to_dict(self) -> dict:
        return {
            'title': self.title,
            'summary': self.summary,
            'link': self.link,
            'from_source': self.from_source,
            'category': self.category,
            'tags': self.tags or [],
            'published_at': self.published_at or '',
            'created_at': self.created_at or datetime.now()
        }
    

class DataSource(ABC):
    @abstractmethod
    def fetch_data(self):
        pass
