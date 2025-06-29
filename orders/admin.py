from django.contrib import admin
from .models import Order, TelegramOrder


@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = ('id', 'user', 'status', 'created_at')
    list_filter = ('status', 'created_at')
    search_fields = ('user__username',)


@admin.register(TelegramOrder)
class TelegramOrderAdmin(admin.ModelAdmin):
    list_display = ('id', 'username', 'user_id', 'bouquet_name', 'delivery_address', 'status', 'created_at')
    list_filter = ('status', 'created_at')
    search_fields = ('username', 'bouquet_name', 'delivery_address')
