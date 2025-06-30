from django.urls import path
from . import views

app_name = 'telegram_bot'

urlpatterns = [
    path('', views.bot_status, name='bot_status'),
]
