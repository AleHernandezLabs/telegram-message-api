from abc import ABC, abstractmethod

class TelegramService(ABC):
    """Abstract interface for Telegram operations."""
    @abstractmethod
    async def send_message(self, chat_id: str, message: str, token: str) -> bool:
        pass