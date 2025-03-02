from abc import ABC, abstractmethod
class TextCommandHandler(ABC):
    @abstractmethod
    def can_handle(self, text: str) -> bool:
        pass

    @abstractmethod
    def handle(self, open_id: str, text: str) -> None:
        pass