from pydantic import BaseModel, Field

class SendMessageRequest(BaseModel):
    """DTO for send message request."""
    api_key: str = Field(..., description="API key for authentication")
    chat_id: str = Field(..., description="Telegram chat ID")
    message: str = Field(..., description="Message content to send")
    telegram_token: str = Field(..., description="Telegram bot token")

class MessageResponse(BaseModel):
    """DTO for message response."""
    status: str = Field(..., description="Status of the operation")
    log_id: int = Field(..., description="ID of the logged message")