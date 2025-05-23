# Generated by Django 5.1.3 on 2025-05-24 15:24

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('catalog', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Order',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('status', models.CharField(choices=[('new', 'Новый'), ('processing', 'В обработке'), ('completed', 'Завершён'), ('cancelled', 'Отменён')], default='new', max_length=20)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('products', models.ManyToManyField(to='catalog.product')),
            ],
        ),
    ]
