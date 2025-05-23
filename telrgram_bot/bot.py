import asyncio
import logging
from aiogram import Bot, Dispatcher
from telegram_bot.handlers import register_handlers

API_TOKEN = 'YOUR_BOT_TOKEN_HERE'  # 🔒 Замените на токен

logging.basicConfig(level=logging.INFO)
bot = Bot(token=API_TOKEN)
dp = Dispatcher(bot)

def main():
    register_handlers(dp)
    asyncio.run(dp.start_polling(bot))

if __name__ == '__main__':
    main()
