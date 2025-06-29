# orders/admin.py
from django.contrib import admin
from .models import Order, TelegramOrder


@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = ('get_bouquet_names', 'user', 'status', 'created_at')
    list_filter = ('status', 'created_at')
    search_fields = ('user__username',)

    def get_bouquet_names(self, obj):
        return ", ".join([product.name for product in obj.products.all()])

    get_bouquet_names.short_description = 'Букеты'


@admin.register(TelegramOrder)
class TelegramOrderAdmin(admin.ModelAdmin):
    list_display = ('bouquet_name', 'telegram_username', 'telegram_user_id', 'created_at')
    list_filter = ('created_at',)
    search_fields = ('bouquet_name', 'telegram_username', 'telegram_user_id')
