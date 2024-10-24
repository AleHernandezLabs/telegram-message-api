from sqlalchemy.orm import Session
from domain.interfaces.message_repository import MessageRepository
from domain.entities.message import Message
from .models import MessageModel

class PostgresMessageRepository(MessageRepository):
    def __init__(self, session: Session):
        self.session = session

    async def save(self, message: Message) -> int:
        db_message = MessageModel(
            message=message.message,
            chat_id=message.chat_id,
            telegram_token=message.telegram_token,
            timestamp=message.timestamp
        )
        self.session.add(db_message)
        self.session.commit()
        self.session.refresh(db_message)
        return db_message.id

    async def get_by_id(self, message_id: int) -> Message:
        db_message = self.session.query(MessageModel).filter(MessageModel.id == message_id).first()
        return Message(
            message=db_message.message,
            chat_id=db_message.chat_id,
            telegram_token=db_message.telegram_token,
            timestamp=db_message.timestamp
        ) if db_message else None
