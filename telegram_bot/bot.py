# telegram_bot/bot.py

import asyncio
import logging
from aiogram import Bot, Dispatcher
from telegram_bot.handlers import register_handlers

API_TOKEN = '7763598812:AAHa-yOc3rZ0wINeAptiE6ktRflzADi_OqU'  # ← сюда вставь настоящий токен

logging.basicConfig(level=logging.INFO)
bot = Bot(token=API_TOKEN)
dp = Dispatcher()

def main():
    register_handlers(dp)
    asyncio.run(dp.start_polling(bot))

if __name__ == '__main__':
    main()
