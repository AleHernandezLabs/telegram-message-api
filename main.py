from fastapi import FastAPI, Depends, HTTPException
from pydantic import BaseModel
import asyncio
from aiogram import Bot, Dispatcher, types
from sqlalchemy import create_engine, Column, Integer, String, DateTime
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from datetime import datetime
import os

# FastAPI instance
app = FastAPI()

# Database setup
DATABASE_URL = os.getenv('DATABASE_URL', 'postgresql://user:password@localhost/dbname')

engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()

class MessageLog(Base):
    __tablename__ = "message_logs"

    id = Column(Integer, primary_key=True, index=True)
    message = Column(String)
    chat_id = Column(String)
    telegram_token = Column(String)
    timestamp = Column(DateTime, default=datetime.utcnow)

# Create the table if it doesn't exist
Base.metadata.create_all(bind=engine)

# Telegram bot setup
async def get_bot(token: str):
    return Bot(token=token)

# Dependency to get DB session
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# Pydantic model for request body
class MessageRequest(BaseModel):
    api_key: str
    chat_id: str
    message: str
    telegram_token: str

# Verify API key (hardcoded or environment variable)
API_KEY = os.getenv('API_KEY', 'your_production_api_key')

def verify_api_key(api_key: str):
    if api_key != API_KEY:
        raise HTTPException(status_code=403, detail="Invalid API Key")

# Send message to Telegram
async def send_telegram_message(chat_id: str, message: str, token: str):
    bot = await get_bot(token)
    dp = Dispatcher(bot)

    try:
        await bot.send_message(chat_id=chat_id, text=message)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
    finally:
        await bot.session.close()

@app.post("/send_message")
async def send_message(request: MessageRequest, db: SessionLocal = Depends(get_db)):
    verify_api_key(request.api_key)

    # Send the message to Telegram
    await send_telegram_message(request.chat_id, request.message, request.telegram_token)

    # Log the message to the database
    log_entry = MessageLog(
        message=request.message,
        chat_id=request.chat_id,
        telegram_token=request.telegram_token
    )
    db.add(log_entry)
    db.commit()
    db.refresh(log_entry)

    return {"status": "Message sent", "log_id": log_entry.id}

@app.get("/")
def read_root():
    return {"message": "Welcome to Telegram Message API"}

# Error handling
@app.exception_handler(Exception)
async def validation_exception_handler(request, exc):
    return {"message": str(exc)}
