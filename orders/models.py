# orders/models.py
from django.db import models

class TelegramOrder(models.Model):
    user_id = models.BigIntegerField()
    username = models.CharField(max_length=150, blank=True)
    bouquet_name = models.CharField(max_length=255)
    address = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.username or self.user_id}: {self.bouquet_name} -> {self.address}"
