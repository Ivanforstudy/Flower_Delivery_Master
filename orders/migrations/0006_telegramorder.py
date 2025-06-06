# Generated by Django 5.1.3 on 2025-06-03 13:38

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('orders', '0005_order_delete_telegramorder'),
    ]

    operations = [
        migrations.CreateModel(
            name='TelegramOrder',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('bouquet_name', models.CharField(max_length=255)),
                ('address', models.TextField()),
                ('telegram_user_id', models.BigIntegerField()),
                ('telegram_username', models.CharField(max_length=150)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
            ],
        ),
    ]
