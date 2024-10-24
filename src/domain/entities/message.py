from datetime import datetime
from pydantic import BaseModel, Field

class Message(BaseModel):
    """Domain entity representing a message."""
    message: str = Field(..., description="The message content to be sent")
    chat_id: str = Field(..., description="Telegram chat ID")
    telegram_token: str = Field(..., description="Telegram bot token")
    timestamp: datetime = Field(default_factory=datetime.utcnow)