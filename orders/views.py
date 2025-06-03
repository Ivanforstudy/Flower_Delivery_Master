from django.http import HttpResponse
from django.shortcuts import render
from .models import TelegramOrder
from django.shortcuts import render
from .models import TelegramOrder


def telegram_orders_view(request):
    orders = TelegramOrder.objects.all().order_by('-created_at')
    return render(request, 'orders/order_list.html', {'orders': orders})

def order_list(request):
    return HttpResponse("Список заказов")
