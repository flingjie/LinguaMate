from abc import ABC, abstractmethod
from enum import Enum


class MessageType(Enum):
    TEXT = "text"
    REACTION = "reaction"

class MessageHandler(ABC):
    @abstractmethod
    def handle(self, open_id: str, content: str) -> None:
        pass

