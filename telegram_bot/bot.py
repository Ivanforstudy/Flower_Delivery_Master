# telegram_bot/bot.py
import os
import django
from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, MessageHandler, filters, ContextTypes, ConversationHandler

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "flower_delivery_master.settings")
django.setup()

from orders.models import TelegramOrder

ASK_ORDER = 1

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("🌸 Добро пожаловать в Flower Delivery Master!\nВведите название букета и адрес доставки:")
    return ASK_ORDER

async def handle_order(update: Update, context: ContextTypes.DEFAULT_TYPE):
    text = update.message.text
    if ',' not in text:
        await update.message.reply_text("Пожалуйста, укажите название букета и адрес, разделив их запятой.")
        return ASK_ORDER

    bouquet, address = map(str.strip, text.split(",", 1))

    TelegramOrder.objects.create(
        user_id=update.effective_user.id,
        username=update.effective_user.username,
        bouquet_name=bouquet,
        address=address
    )

    await update.message.reply_text("✅ Ваш заказ принят! Спасибо 🌸")
    return ConversationHandler.END

async def cancel(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("❌ Заказ отменён.")
    return ConversationHandler.END

def main():
    from config import BOT_TOKEN  # Лучше хранить токен в отдельном файле
    app = ApplicationBuilder().token(BOT_TOKEN).build()

    conv_handler = ConversationHandler(
        entry_points=[CommandHandler("start", start)],
        states={
            ASK_ORDER: [MessageHandler(filters.TEXT & ~filters.COMMAND, handle_order)],
        },
        fallbacks=[CommandHandler("cancel", cancel)],
    )

    app.add_handler(conv_handler)
    app.run_polling()
