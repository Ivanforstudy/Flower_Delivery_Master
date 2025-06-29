from django.conf import settings
from catalog.models import Product
from django.db import models


class Order(models.Model):
    STATUS_CHOICES = [
        ('pending', 'В ожидании'),
        ('in_progress', 'В обработке'),
        ('completed', 'Выполнен'),
        ('cancelled', 'Отменён'),
    ]

    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    products = models.ManyToManyField(Product, related_name='orders')
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pending')
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'Заказ {self.pk} от {self.user}'


class TelegramOrder(models.Model):
    bouquet_name = models.CharField(max_length=255)
    telegram_username = models.CharField(max_length=255)
    telegram_user_id = models.BigIntegerField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'Telegram заказ: {self.bouquet_name} от {self.telegram_username}'
