import logging
import os
import django
import traceback
import datetime

from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, MessageHandler, ContextTypes, filters
from asgiref.sync import sync_to_async

# Настройка Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'flower_delivery_master.settings')
django.setup()

from orders.models import TelegramOrder

# Логирование
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)

# Глобальное хранилище сессий пользователей
user_sessions = {}

# Время работы магазина
WORK_HOURS_START = 9
WORK_HOURS_END = 21

def is_within_working_hours():
    now = datetime.datetime.now().time()
    return datetime.time(WORK_HOURS_START) <= now <= datetime.time(WORK_HOURS_END)

# Команда /start
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    chat_id = update.message.chat_id
    user_sessions[chat_id] = {"step": "bouquet"}
    await update.message.reply_text("🌸 Добро пожаловать в Flower Delivery Master!\nВведите название букета:")

# Сохранение заказа
@sync_to_async
def save_order(session, user):
    TelegramOrder.objects.create(
        bouquet_name=session["bouquet_name"],
        address=session["address"],
        telegram_user_id=user.id,
        telegram_username=user.username or user.full_name or "Неизвестно"
    )

# Получение заказов пользователя
@sync_to_async
def get_user_orders(user_id):
    return list(TelegramOrder.objects.filter(telegram_user_id=user_id).order_by('-created_at'))

# Команда /status — показать заказы пользователя
async def status(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.message.from_user.id
    orders = await get_user_orders(user_id)

    if not orders:
        await update.message.reply_text("У вас пока нет заказов.")
        return

    message = "📦 Ваши заказы:\n"
    for o in orders:
        message += f"• {o.bouquet_name} — {o.created_at.strftime('%d.%m.%Y %H:%M')}\n"

    await update.message.reply_text(message)

# Обработка текстовых сообщений
async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    print("🟢 handle_message вызван")

    chat_id = update.message.chat_id
    text = update.message.text
    print(f"📩 Сообщение от chat_id={chat_id}: {text}")

    if not is_within_working_hours():
        await update.message.reply_text("⛔ Заказы принимаются только с 09:00 до 21:00. Попробуйте позже.")
        return

    if chat_id not in user_sessions:
        print("⚠️ Пользователь не начал с /start")
        await update.message.reply_text("Пожалуйста, введите /start чтобы начать.")
        return

    session = user_sessions[chat_id]
    print(f"🔄 Текущий шаг: {session['step']}")

    if session["step"] == "bouquet":
        session["bouquet_name"] = text
        session["step"] = "address"
        print(f"✅ Название букета сохранено: {text}")
        await update.message.reply_text("Введите адрес доставки:")

    elif session["step"] == "address":
        session["address"] = text

        try:
            print("📥 Пытаюсь сохранить заказ...")
            await save_order(session, update.message.from_user)
            print("✅ Заказ успешно сохранён")
            await update.message.reply_text("✅ Заказ принят! Спасибо за оформление!")
        except Exception as e:
            print("❌ Ошибка при сохранении заказа:")
            traceback.print_exc()
            await update.message.reply_text("Произошла ошибка при оформлении заказа.")

        del user_sessions[chat_id]

# Запуск бота
def main():
    TOKEN = '7763598812:AAHa-yOc3rZ0wINeAptiE6ktRflzADi_OqU'

    app = ApplicationBuilder().token(TOKEN).build()

    app.add_handler(CommandHandler("start", start))
    app.add_handler(CommandHandler("status", status))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))

    print("🤖 Бот запущен")
    app.run_polling()
