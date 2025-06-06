# Generated by Django 5.1.3 on 2025-05-28 15:26

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('orders', '0002_order_comment_order_total_price_alter_order_products_and_more'),
    ]

    operations = [
        migrations.CreateModel(
            name='TelegramOrder',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('user_id', models.BigIntegerField()),
                ('username', models.CharField(blank=True, max_length=150)),
                ('bouquet_name', models.CharField(max_length=255)),
                ('address', models.TextField()),
                ('created_at', models.DateTimeField(auto_now_add=True)),
            ],
        ),
        migrations.DeleteModel(
            name='Order',
        ),
    ]
