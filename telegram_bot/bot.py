import os
import django
import logging
from datetime import datetime, time, timedelta, timezone

from telegram import Update
from telegram.ext import (
    Application,
    CommandHandler,
    MessageHandler,
    filters,
    ConversationHandler,
    ContextTypes,
)

# Django setup
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "flower_delivery_master.settings")
django.setup()

from orders.models import TelegramOrder

# Логирование
logging.basicConfig(
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    level=logging.INFO,
)

# Telegram Bot Token и Admin ID
BOT_TOKEN = '7763598812:AAHa-yOc3rZ0wINeAptiE6ktRflzADi_OqU'
ADMIN_ID = 2111297101

# Этапы ConversationHandler
BOUQUET_NAME, DELIVERY_ADDRESS = range(2)


# Проверка, рабочий день или нет
def is_working_day_and_time():
    now = datetime.now(timezone.utc) + timedelta(hours=3)  # МСК
    weekday = now.weekday()  # 0-понедельник, 6-воскресенье
    current_time = now.time()

    if weekday in [5, 6]:
        return False, "Сегодня выходной.\nЗаказы принимаются с ПОНЕДЕЛЬНИКА по ПЯТНИЦУ с 09:00 до 19:00."

    if not (time(9, 0) <= current_time <= time(19, 0)):
        return False, "Заказы принимаются только с 09:00 до 19:00.\nПопробуйте позже."

    return True, None


# Старт
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    user = update.effective_user

    is_open, message = is_working_day_and_time()
    if not is_open:
        await update.message.reply_text(
            f"🌸 Добро пожаловать в Flower Delivery Master!\n\n{message}"
        )
        return ConversationHandler.END

    await update.message.reply_text(
        "🌸 Добро пожаловать в Flower Delivery Master!\nВведите название букета:"
    )

    context.user_data["telegram_username"] = user.username or "NoUsername"
    context.user_data["telegram_user_id"] = user.id

    return BOUQUET_NAME


# Получение названия букета
async def bouquet_name(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    context.user_data["bouquet_name"] = update.message.text

    await update.message.reply_text("Введите адрес доставки:")

    return DELIVERY_ADDRESS


# Получение адреса и сохранение заказа
async def delivery_address(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    delivery_address = update.message.text

    TelegramOrder.objects.create(
        bouquet_name=context.user_data["bouquet_name"],
        telegram_username=context.user_data["telegram_username"],
        telegram_user_id=context.user_data["telegram_user_id"],
        delivery_address=delivery_address,
    )

    await update.message.reply_text(
        f"✅ Заказ принят!\n\nБукет: {context.user_data['bouquet_name']}\n"
        f"Адрес доставки: {delivery_address}"
    )

    return ConversationHandler.END


# Статистика для админа
async def stats(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    user_id = update.effective_user.id
    if user_id != ADMIN_ID:
        await update.message.reply_text("❌ У вас нет доступа к статистике.")
        return

    now = datetime.now(timezone.utc) + timedelta(hours=3)
    start_of_day = now.replace(hour=0, minute=0, second=0, microsecond=0)

    orders_today = TelegramOrder.objects.filter(created_at__gte=start_of_day)
    total_orders = orders_today.count()
    total_revenue = total_orders * 1500  # Предположим, каждый заказ = 1500 руб

    await update.message.reply_text(
        f"📊 Статистика за сегодня ({now.strftime('%d.%m.%Y')}):\n"
        f"🛍️ Заказов: {total_orders}\n"
        f"💰 Выручка: {total_revenue} руб."
    )


# Отмена
async def cancel(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    await update.message.reply_text("❌ Заказ отменён.")
    return ConversationHandler.END


# Основная функция запуска бота
def main() -> None:
    app = Application.builder().token(BOT_TOKEN).build()

    conv_handler = ConversationHandler(
        entry_points=[CommandHandler("start", start)],
        states={
            BOUQUET_NAME: [
                MessageHandler(filters.TEXT & ~filters.COMMAND, bouquet_name)
            ],
            DELIVERY_ADDRESS: [
                MessageHandler(filters.TEXT & ~filters.COMMAND, delivery_address)
            ],
        },
        fallbacks=[CommandHandler("cancel", cancel)],
    )

    app.add_handler(conv_handler)
    app.add_handler(CommandHandler("stats", stats))

    print("🤖 Bot started...")
    app.run_polling()


if __name__ == "__main__":
    main()
