from typing import List
from .data_sources.source_interface import DataSource, News
from .data_observer import DataObserver

class DataCollector:
    def __init__(self):
        self._data_sources: List[DataSource] = []
        self._observers: List[DataObserver] = []

    def add_data_source(self, data_source: DataSource):
        self._data_sources.append(data_source)

    def add_observer(self, observer: DataObserver):
        self._observers.append(observer)

    def notify_observers(self, data: List[News]):
        for observer in self._observers:
            observer.update(data)

    def fetch_data(self):
        for source in self._data_sources:
            data = source.fetch_data()
            self.notify_observers(data)
