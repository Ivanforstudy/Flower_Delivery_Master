import logging
from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, MessageHandler, ContextTypes, filters
import os
import django

import os
import sys
from pathlib import Path

# Меняем рабочую директорию на корень проекта
BASE_DIR = Path(__file__).resolve().parent.parent
os.chdir(BASE_DIR)

sys.path.append(str(BASE_DIR))  # чтобы Django находил проект
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'flower_delivery_master.settings')
django.setup()

from orders.models import TelegramOrder

logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)

# Память сессий (простая версия)
user_sessions = {}

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("🌸 Добро пожаловать в Flower Delivery Master!\nВведите название букета и адрес доставки:")
    user_sessions[update.message.chat_id] = {"step": "bouquet"}

async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    chat_id = update.message.chat_id
    text = update.message.text

    if chat_id not in user_sessions:
        await update.message.reply_text("Пожалуйста, введите /start чтобы начать.")
        return

    session = user_sessions[chat_id]

    if session["step"] == "bouquet":
        session["bouquet_name"] = text
        session["step"] = "address"
        await update.message.reply_text("Введите адрес доставки:")
    elif session["step"] == "address":
        session["address"] = text

        try:
            print("📥 Пытаюсь сохранить заказ...")
            from orders.models import TelegramOrder
            TelegramOrder.objects.create(
                telegram_username=update.message.from_user.full_name,
                bouquet_name=session["bouquet_name"],
                address=session["address"]
            )
            print("✅ Заказ успешно сохранён")
            await update.message.reply_text("✅ Заказ принят! Спасибо за оформление!")
        except Exception as e:
            print(f"❌ Ошибка при сохранении заказа: {e}")
            await update.message.reply_text("Произошла ошибка при оформлении заказа.")

        del user_sessions[chat_id]


def run_bot():
    import asyncio
    from telegram.ext import ApplicationBuilder

    # Вставьте ваш токен
    TOKEN = '7763598812:AAHa-yOc3rZ0wINeAptiE6ktRflzADi_OqU'

    app = ApplicationBuilder().token(TOKEN).build()

    app.add_handler(CommandHandler("start", start))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))

    print("🤖 Бот запущен")
    app.run_polling()
