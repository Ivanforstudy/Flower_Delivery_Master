from django.contrib.auth.decorators import login_required, user_passes_test
from django.shortcuts import render
from datetime import datetime, timedelta

from orders.models import Order, TelegramOrder


def staff_check(user):
    return user.is_staff


@login_required
@user_passes_test(staff_check)
def dashboard(request):
    now = datetime.now()
    start_of_day = now.replace(hour=0, minute=0, second=0, microsecond=0)

    # Аналитика по веб-заказам
    web_orders = Order.objects.filter(created_at__gte=start_of_day)
    web_orders_count = web_orders.count()
    web_orders_revenue = web_orders_count * 2000  # допустим, средний чек 2000 руб.

    # Аналитика по телеграм-заказам
    telegram_orders = TelegramOrder.objects.filter(created_at__gte=start_of_day)
    telegram_orders_count = telegram_orders.count()
    telegram_orders_revenue = telegram_orders_count * 1500  # средний чек 1500 руб.

    total_orders = web_orders_count + telegram_orders_count
    total_revenue = web_orders_revenue + telegram_orders_revenue

    context = {
        'date': now.strftime('%d.%m.%Y'),
        'web_orders_count': web_orders_count,
        'web_orders_revenue': web_orders_revenue,
        'telegram_orders_count': telegram_orders_count,
        'telegram_orders_revenue': telegram_orders_revenue,
        'total_orders': total_orders,
        'total_revenue': total_revenue,
    }

    return render(request, 'analytics/dashboard.html', context)
