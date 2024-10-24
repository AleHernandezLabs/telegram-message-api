from abc import ABC, abstractmethod
from domain.entities.message import Message

class MessageRepository(ABC):
    """Abstract interface for message persistence."""
    @abstractmethod
    async def save(self, message: Message) -> int:
        pass

    @abstractmethod
    async def get_by_id(self, message_id: int) -> Message:
        pass