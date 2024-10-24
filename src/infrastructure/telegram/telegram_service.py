from aiogram import Bot
from domain.interfaces.telegram_service import TelegramService

class AiogramTelegramService(TelegramService):
    async def send_message(self, chat_id: str, message: str, token: str) -> bool:
        bot = Bot(token=token)
        try:
            await bot.send_message(chat_id=chat_id, text=message)
            return True
        finally:
            await bot.session.close()