from django.urls import path
from . import views

app_name = 'orders'

urlpatterns = [
    path('telegram-orders/', views.telegram_orders_view, name='telegram_orders'),
    # если есть другие пути — оставь их
]
