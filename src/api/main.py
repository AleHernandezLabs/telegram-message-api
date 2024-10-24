from fastapi import FastAPI, Depends, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy.orm import Session
from application.dtos.message_dto import SendMessageRequest, MessageResponse
from application.use_cases.send_message_use_case import SendMessageUseCase
from infrastructure.persistence.postgresql.repository import PostgresMessageRepository
from infrastructure.telegram.telegram_service import AiogramTelegramService
from infrastructure.persistence.postgresql.database import get_db
from src.config import Settings
import logging

# Initialize the logger
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

app = FastAPI(
    title="Telegram Message API",
    description="""
    API for sending messages through Telegram bots and logging them.

    Created by: Alejandro Exequiel Hernández Lara
    """,
    version="1.0.0",
    docs_url="/docs",
    redoc_url="/redoc"
)

# Load settings from environment variables
settings = Settings()

# CORS configuration
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# API key verification
def verify_api_key(api_key: str):
    if api_key != settings.api_key:
        raise HTTPException(
            status_code=403,
            detail="Invalid API Key"
        )

# Dependency injection for repository and Telegram service
def get_repository(db: Session = Depends(get_db)):
    return PostgresMessageRepository(db)

def get_telegram_service():
    return AiogramTelegramService()

@app.post(
    "/send_message",
    response_model=MessageResponse,
    summary="Send a message through Telegram",
    description="Sends a message through a Telegram bot and logs it to the database",
    response_description="Returns the status and log ID of the sent message"
)
async def send_message(
    request: SendMessageRequest,
    db: Session = Depends(get_db),
    repository: PostgresMessageRepository = Depends(get_repository),
    telegram_service: AiogramTelegramService = Depends(get_telegram_service)
):
    verify_api_key(request.api_key)
    use_case = SendMessageUseCase(repository, telegram_service)

    try:
        result = await use_case.execute(request)
        logger.info(f"Message sent successfully: {result}")
        return result
    except Exception as e:
        logger.error(f"Failed to send message: {e}")
        raise HTTPException(status_code=500, detail=str(e))

@app.get(
    "/",
    summary="Root endpoint",
    description="Welcome message for the API"
)
def read_root():
    return {
        "message": "Welcome to Telegram Message API",
        "version": "1.0.0",
        "author": settings.author,
        "website": settings.website,
        "email": settings.email
    }
