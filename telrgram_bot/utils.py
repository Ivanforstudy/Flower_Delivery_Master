from datetime import datetime
import pytz
from orders.models import Order
from django.contrib.auth import get_user_model

def is_working_hours():
    tz = pytz.timezone('Europe/Moscow')
    now = datetime.now(tz)
    return now.weekday() < 6 and 9 <= now.hour < 19

def save_order_to_db(user_id, text):
    # Простейшая логика — можно усовершенствовать
    Order.objects.create(
        user=None,  # Можно сопоставить с User по Telegram ID, если реализовано
        status='Новый',
        total_price=0,
        comment=f"Заказ из Telegram от {user_id}: {text}"
    )
