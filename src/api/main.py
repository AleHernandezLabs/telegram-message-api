from fastapi import FastAPI, Depends, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy.orm import Session
from application.dtos.message_dto import SendMessageRequest, MessageResponse
from application.use_cases.send_message_use_case import SendMessageUseCase
from infrastructure.persistence.postgresql.repository import PostgresMessageRepository
from infrastructure.telegram.telegram_service import AiogramTelegramService
from infrastructure.persistence.postgresql.database import get_db
import os

app = FastAPI(
    title="Telegram Message API",
    description="""
    API for sending messages through Telegram bots and logging them.

    Created by: Alejandro Exequiel Hernández Lara
    Website: www.alehernandezlabs.com
    Email: alehernandezlabs@gmail.com
    """,
    version="1.0.0",
    docs_url="/docs",
    redoc_url="/redoc"
)

# CORS configuration
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# API key verification
API_KEY = os.getenv('API_KEY', 'your_production_api_key')

def verify_api_key(api_key: str):
    if api_key != API_KEY:
        raise HTTPException(
            status_code=403,
            detail="Invalid API Key"
        )

@app.post(
    "/send_message",
    response_model=MessageResponse,
    summary="Send a message through Telegram",
    description="Sends a message through a Telegram bot and logs it to the database",
    response_description="Returns the status and log ID of the sent message"
)
async def send_message(
    request: SendMessageRequest,
    db: Session = Depends(get_db)
):
    verify_api_key(request.api_key)

    repository = PostgresMessageRepository(db)
    telegram_service = AiogramTelegramService()
    use_case = SendMessageUseCase(repository, telegram_service)

    try:
        return await use_case.execute(request)
    except Exception as e:
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
        "author": "Alejandro Exequiel Hernández Lara",
        "website": "www.alehernandezlabs.com",
        "email": "alehernandezlabs@gmail.com"
    }