import telebot
from catalog.models import Product
from telegram_bot.models import TelegramOrder
from django.conf import settings
import django
import os

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'flower_delivery_master.settings')
django.setup()

bot = telebot.TeleBot('YOUR_TELEGRAM_BOT_TOKEN')

user_data = {}


@bot.message_handler(commands=['start'])
def start(message):
    bot.send_message(message.chat.id, "Здравствуйте! Введите название букета, который хотите заказать.")
    user_data[message.chat.id] = {}


@bot.message_handler(func=lambda message: message.chat.id in user_data and 'product' not in user_data[message.chat.id])
def get_product(message):
    chat_id = message.chat.id
    product_name = message.text
    try:
        product = Product.objects.get(name__icontains=product_name)
        user_data[chat_id]['product'] = product
        bot.send_message(chat_id, "Введите адрес доставки:")
    except Product.DoesNotExist:
        bot.send_message(chat_id, "Такого букета не найдено. Попробуйте снова.")


@bot.message_handler(func=lambda message: message.chat.id in user_data and 'product' in user_data[message.chat.id] and 'address' not in user_data[message.chat.id])
def get_address(message):
    chat_id = message.chat.id
    address = message.text
    user_data[chat_id]['address'] = address

    product = user_data[chat_id]['product']

    TelegramOrder.objects.create(
        user_id=chat_id,
        product=product,
        address=address
    )

    bot.send_message(chat_id, f"Ваш заказ '{product.name}' успешно принят! Доставка по адресу: {address}. Спасибо!")
    user_data.pop(chat_id)


if __name__ == '__main__':
    bot.polling(none_stop=True)
