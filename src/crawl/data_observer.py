from abc import ABC, abstractmethod
from typing import List


class DataObserver(ABC):
    @abstractmethod
    def update(self, data: List[dict]):
        pass
