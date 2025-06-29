from django.urls import path
from . import views

urlpatterns = [
    path('update-status/', views.update_telegram_order_status, name='update_telegram_order_status'),
]
