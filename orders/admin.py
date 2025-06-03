from django.contrib import admin
from .models import Order, TelegramOrder

@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = ('bouquet_name', 'user', 'status', 'created_at')
    list_filter = ('status', 'created_at')
    search_fields = ('bouquet_name', 'user__username')

@admin.register(TelegramOrder)
class TelegramOrderAdmin(admin.ModelAdmin):
    list_display = ('bouquet_name', 'telegram_username', 'telegram_user_id', 'created_at')
    list_filter = ('created_at',)
    search_fields = ('bouquet_name', 'telegram_username', 'telegram_user_id')
