from aiogram import types, Dispatcher
from datetime import datetime
import pytz
from telegram_bot.utils import save_order_to_db, is_working_hours

async def start(message: types.Message):
    await message.answer("🌸 Добро пожаловать в Flower Delivery Master!\nВведите название букета и адрес доставки:")

async def handle_order(message: types.Message):
    if not is_working_hours():
        return await message.answer("⏰ Заказы принимаются с 09:00 до 19:00 (Мск). Пожалуйста, попробуйте позже.")

    text = message.text.strip()
    await save_order_to_db(user_id=message.from_user.id, text=text)
    await message.answer("✅ Ваш заказ принят! Мы свяжемся с вами.")

def register_handlers(dp: Dispatcher):
    dp.message.register(start, commands=['start'])
    dp.message.register(handle_order)
