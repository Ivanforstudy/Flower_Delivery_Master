# orders/models.py

from django.db import models
from django.contrib.auth import get_user_model
from catalog.models import Product  # Импортировать модель продукта

class Order(models.Model):
    user = models.ForeignKey(get_user_model(), on_delete=models.SET_NULL, null=True, blank=True)
    status = models.CharField(max_length=50, default='Новый')
    total_price = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    comment = models.TextField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    products = models.ManyToManyField(Product, related_name='orders', blank=True)
    def __str__(self):
        return f"Заказ #{self.id} - {self.status}"
