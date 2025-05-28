# telegram_bot/utils.py

from datetime import datetime
import pytz
from orders.models import Order

def is_working_hours():
    tz = pytz.timezone('Europe/Moscow')
    now = datetime.now(tz)
    return now.weekday() < 6 and 9 <= now.hour < 19

async def save_order_to_db(user_id, text):
    Order.objects.create(
        user=None,  # Можно сопоставить с пользователем, если привяжем Telegram ID
        status='Новый',
        total_price=0,
        comment=f"Заказ из Telegram от {user_id}: {text}"
    )
