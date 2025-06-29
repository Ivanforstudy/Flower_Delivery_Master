import os
import django
import logging
from datetime import datetime, time

from telegram import Update
from telegram.ext import Application, CommandHandler, MessageHandler, filters, ConversationHandler, ContextTypes

# Django настройки
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'flower_delivery_master.settings')
django.setup()

from catalog.models import Product
from orders.models import TelegramOrder

# Логирование
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)
logger = logging.getLogger(__name__)

# Состояния для ConversationHandler
BOUQUET, ADDRESS = range(2)

# 🔔 Данные для уведомлений
BOT_TOKEN = '7763598812:AAHa-yOc3rZ0wINeAptiE6ktRflzADi_OqU'
ADMIN_CHAT_ID = 2111297101


# Проверка рабочего времени
def is_working_hours():
    now = datetime.now()
    current_time = now.time()
    current_day = now.weekday()  # Пн=0, ..., Вс=6

    if current_day >= 5:
        return 'weekend'

    if time(9, 0) <= current_time <= time(19, 0):
        return 'open'

    return 'closed'


# Старт
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    status = is_working_hours()

    if status == 'weekend':
        await update.message.reply_text(
            "🌸 Добро пожаловать в Flower Delivery Master!\n"
            "Сегодня выходной.\n"
            "Заказы принимаются с понедельника по пятницу с 09:00 до 19:00."
        )
        return ConversationHandler.END

    if status == 'closed':
        await update.message.reply_text(
            "Заказы принимаются только с 09:00 до 19:00.\nПопробуйте позже."
        )
        return ConversationHandler.END

    products = Product.objects.all()
    if products:
        product_list = "\n".join([f"• {product.name} — {product.price} руб." for product in products])
        await update.message.reply_text(
            f"🌸 Добро пожаловать в Flower Delivery Master!\n\n"
            f"📜 Вот наш каталог:\n{product_list}\n\n"
            f"Пожалуйста, введите название букета:"
        )
    else:
        await update.message.reply_text(
            "Каталог пуст. Пожалуйста, попробуйте позже."
        )
        return ConversationHandler.END

    return BOUQUET


# Получение названия букета
async def bouquet(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    bouquet_name = update.message.text.strip()

    if not Product.objects.filter(name__iexact=bouquet_name).exists():
        await update.message.reply_text(
            "❌ Такого букета нет в каталоге.\n"
            "Пожалуйста, введите название из предложенного списка."
        )
        return BOUQUET

    context.user_data['bouquet'] = bouquet_name
    await update.message.reply_text("Введите адрес доставки:")
    return ADDRESS


# Получение адреса и сохранение заказа
async def address(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    address = update.message.text
    bouquet_name = context.user_data['bouquet']
    user_id = update.message.from_user.id
    username = update.message.from_user.username or "Без имени"

    TelegramOrder.objects.create(
        user_id=user_id,
        username=username,
        bouquet_name=bouquet_name,
        delivery_address=address
    )

    await update.message.reply_text(
        f"✅ Спасибо за заказ!\n\n"
        f"Букет: {bouquet_name}\n"
        f"Адрес доставки: {address}\n\n"
        f"Наш менеджер свяжется с вами."
    )

    # 🔔 Уведомление админу
    admin_message = (
        f"🆕 Новый заказ!\n\n"
        f"👤 Пользователь: @{username}\n"
        f"📦 Букет: {bouquet_name}\n"
        f"📍 Адрес: {address}"
    )

    try:
        await context.bot.send_message(chat_id=ADMIN_CHAT_ID, text=admin_message)
    except Exception as e:
        logger.error(f"Не удалось отправить сообщение администратору: {e}")

    return ConversationHandler.END


# Отмена
async def cancel(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    await update.message.reply_text("❌ Заказ отменён.")
    return ConversationHandler.END


# 📊 Статистика по заказам за сегодня
async def stats(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if update.effective_user.id != ADMIN_CHAT_ID:
        await update.message.reply_text("❌ У вас нет прав для этой команды.")
        return

    today = datetime.now().date()
    orders_today = TelegramOrder.objects.filter(created_at__date=today)
    total_orders = orders_today.count()

    total_revenue = 0
    for order in orders_today:
        product = Product.objects.filter(name__iexact=order.bouquet_name).first()
        if product:
            total_revenue += product.price

    message = (
        f"📊 Статистика за {today.strftime('%d.%m.%Y')}:\n\n"
        f"🛒 Заказов: {total_orders}\n"
        f"💰 Выручка: {total_revenue} руб."
    )

    await update.message.reply_text(message)


# 🔄 Проверка статуса заказа
async def status(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.effective_user.id
    orders = TelegramOrder.objects.filter(user_id=user_id).order_by('-created_at')

    if not orders.exists():
        await update.message.reply_text("❌ У вас нет активных заказов.")
        return

    last_order = orders.first()

    status_dict = {
        'pending': 'В ожидании',
        'in_progress': 'В обработке',
        'completed': 'Выполнен',
        'cancelled': 'Отменён',
    }

    status = status_dict.get(last_order.status, 'Неизвестно')

    await update.message.reply_text(
        f"📦 Статус вашего последнего заказа:\n\n"
        f"Букет: {last_order.bouquet_name}\n"
        f"Адрес: {last_order.delivery_address}\n"
        f"Статус: {status}"
    )


def main():
    application = Application.builder().token(BOT_TOKEN).build()

    conv_handler = ConversationHandler(
        entry_points=[CommandHandler('start', start)],
        states={
            BOUQUET: [MessageHandler(filters.TEXT & ~filters.COMMAND, bouquet)],
            ADDRESS: [MessageHandler(filters.TEXT & ~filters.COMMAND, address)],
        },
        fallbacks=[CommandHandler('cancel', cancel)],
    )

    application.add_handler(conv_handler)
    application.add_handler(CommandHandler('stats', stats))
    application.add_handler(CommandHandler('status', status))

    print("Бот запущен...")
    application.run_polling()


if __name__ == '__main__':
    main()
