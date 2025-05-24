from django.db import models


class Category(models.Model):
    name = models.CharField(max_length=100, unique=True, verbose_name='Категория')
    description = models.TextField(blank=True, verbose_name='Описание')

    def __str__(self):
        return self.name


class Product(models.Model):
    name = models.CharField(max_length=255, verbose_name='Название букета')
    description = models.TextField(blank=True, verbose_name='Описание')
    price = models.DecimalField(max_digits=8, decimal_places=2, verbose_name='Цена')
    image = models.ImageField(upload_to='products/', blank=True, null=True, verbose_name='Изображение')
    category = models.ForeignKey(Category, on_delete=models.SET_NULL, null=True, blank=True, verbose_name='Категория')
    is_available = models.BooleanField(default=True, verbose_name='В наличии')
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='Дата добавления')

    def __str__(self):
        return self.name
