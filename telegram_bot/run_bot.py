import os
import sys
import django
import logging

# Добавляем корень проекта в sys.path, чтобы Django-пакет нашёлся
sys.path.append(os.path.dirname(os.path.abspath(__file__)) + "/..")

# Настройка Django
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "flower_delivery_master.settings")
django.setup()

from telegram import Update
from telegram.ext import (
    ApplicationBuilder, CommandHandler, MessageHandler,
    filters, ContextTypes, ConversationHandler
)
from asgiref.sync import sync_to_async
from orders.models import TelegramOrder

# Логирование
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)

# Состояния
BOUQUET, ADDRESS = range(2)

# Старт
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    await update.message.reply_text("Привет! Какой букет вы хотите заказать?")
    return BOUQUET

# Букет
async def get_bouquet(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    context.user_data["bouquet_name"] = update.message.text
    await update.message.reply_text("Отлично! Теперь введите адрес доставки.")
    return ADDRESS

# Адрес
async def get_address(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    address = update.message.text
    bouquet_name = context.user_data.get("bouquet_name")
    user_id = update.effective_user.id

    success = await save_order(user_id, bouquet_name, address)

    if success:
        await update.message.reply_text("✅ Ваш заказ принят! Спасибо!")
    else:
        await update.message.reply_text("❌ Произошла ошибка при оформлении заказа.")
    return ConversationHandler.END

@sync_to_async
def save_order(user_id, bouquet_name, address):
    try:
        TelegramOrder.objects.create(
            telegram_user_id=user_id,
            bouquet_name=bouquet_name,
            address=address
        )
        return True
    except Exception as e:
        logging.error(f"Ошибка при сохранении заказа: {e}")
        return False

# Отмена
async def cancel(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    await update.message.reply_text("❌ Заказ отменён.")
    return ConversationHandler.END

# Запуск
if __name__ == "__main__":
    print("🤖 Бот запущен")

    app = ApplicationBuilder().token("7763598812:AAHa-yOc3rZ0wINeAptiE6ktRflzADi_OqU").build()

    conv_handler = ConversationHandler(
        entry_points=[CommandHandler("start", start)],
        states={
            BOUQUET: [MessageHandler(filters.TEXT & ~filters.COMMAND, get_bouquet)],
            ADDRESS: [MessageHandler(filters.TEXT & ~filters.COMMAND, get_address)],
        },
        fallbacks=[CommandHandler("cancel", cancel)],
    )

    app.add_handler(conv_handler)
    app.run_polling()


