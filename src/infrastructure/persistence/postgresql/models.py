from sqlalchemy import Column, Integer, String, DateTime
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()

class MessageModel(Base):
    """SQLAlchemy model for message persistence."""
    __tablename__ = "message_logs"

    id = Column(Integer, primary_key=True, index=True)
    message = Column(String, nullable=False)
    chat_id = Column(String, nullable=False)
    telegram_token = Column(String, nullable=False)
    timestamp = Column(DateTime, nullable=False)