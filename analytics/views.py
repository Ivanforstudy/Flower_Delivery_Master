from django.shortcuts import render
from orders.models import Order, TelegramOrder
from django.utils.timezone import now
from datetime import timedelta


def dashboard(request):
    today = now().date()
    web_orders = Order.objects.filter(created_at__date=today).count()
    telegram_orders = TelegramOrder.objects.filter(created_at__date=today).count()

    web_revenue = sum(order.products.aggregate(total=models.Sum('price'))['total'] or 0 for order in Order.objects.filter(created_at__date=today))
    telegram_revenue = TelegramOrder.objects.filter(created_at__date=today).count() * 1000  # Допустим, каждая позиция в Telegram по 1000 руб.

    total_orders = web_orders + telegram_orders
    total_revenue = web_revenue + telegram_revenue

    context = {
        'total_orders': total_orders,
        'total_revenue': total_revenue,
        'web_orders': web_orders,
        'telegram_orders': telegram_orders,
        'web_revenue': web_revenue,
        'telegram_revenue': telegram_revenue,
    }
    return render(request, 'analytics/dashboard.html', context)

