@echo off
set DJANGO_SETTINGS_MODULE=flower_delivery_master.settings
set PYTHONPATH=%cd%
venv\Scripts\python.exe telegram_bot\bot.py
pause
