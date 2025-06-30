from django.contrib.admin.views.decorators import staff_member_required
from django.shortcuts import render
from orders.models import Order, TelegramOrder
from django.utils import timezone

@staff_member_required
def dashboard(request):
    today = timezone.now().date()
    orders_today = Order.objects.filter(created_at__date=today).count()
    telegram_orders_today = TelegramOrder.objects.filter(created_at__date=today).count()

    context = {
        'orders_today': orders_today,
        'telegram_orders_today': telegram_orders_today,
    }
    return render(request, 'analytics/dashboard.html', context)
