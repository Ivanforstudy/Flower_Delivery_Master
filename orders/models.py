from django.db import models
from django.conf import settings
from catalog.models import Product

class Order(models.Model):
    STATUS_CHOICES = (
        ('new', 'Новый'),
        ('processing', 'В обработке'),
        ('completed', 'Завершён'),
        ('cancelled', 'Отменён'),
    )

    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    products = models.ManyToManyField(Product)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='new')
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Order #{self.id} ({self.user.username})"
