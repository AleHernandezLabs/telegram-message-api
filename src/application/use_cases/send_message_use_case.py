from domain.entities.message import Message
from domain.interfaces.message_repository import MessageRepository
from domain.interfaces.telegram_service import TelegramService
from application.dtos.message_dto import SendMessageRequest, MessageResponse

class SendMessageUseCase:
    def __init__(self, message_repository: MessageRepository, telegram_service: TelegramService):
        self.message_repository = message_repository
        self.telegram_service = telegram_service

    async def execute(self, request: SendMessageRequest) -> MessageResponse:
        # Create domain entity
        message = Message(
            message=request.message,
            chat_id=request.chat_id,
            telegram_token=request.telegram_token
        )

        # Send message through Telegram
        success = await self.telegram_service.send_message(
            message.chat_id,
            message.message,
            message.telegram_token
        )

        if not success:
            raise Exception("Failed to send message")

        # Save to repository
        log_id = await self.message_repository.save(message)

        return MessageResponse(status="Message sent", log_id=log_id)
