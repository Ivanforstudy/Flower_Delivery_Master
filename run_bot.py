import os
import django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'flower_delivery_master.settings')
django.setup()

from telegram_bot.bot import main

main()


