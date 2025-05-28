from django.contrib import admin
from .models import TelegramOrder


@admin.register(TelegramOrder)
class TelegramOrderAdmin(admin.ModelAdmin):
    list_display = ('id', 'username', 'bouquet_name', 'address', 'created_at')
    search_fields = ('username', 'bouquet_name', 'address')
    list_filter = ('created_at',)


