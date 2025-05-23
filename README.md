# Flower Delivery Web App + Telegram Bot

## 📦 Описание проекта

Система онлайн-заказа доставки цветов через веб-сайт и Telegram-бота. Поддержка управления заказами, отзывов, рейтингов и аналитики.

## 🚀 Технологии

- Django (бэкенд)
- HTML/CSS (шаблоны)
- Python Telegram Bot
- SQLite / PostgreSQL
- Bootstrap (UI)

## 📌 Функциональность

- Авторизация и регистрация
- Каталог цветов
- Корзина и оформление заказа
- Telegram-бот для приёма заказов
- Система отзывов
- Аналитика по заказам
- Админ-панель

## 📂 Запуск проекта

```bash
git clone https://github.com/your-username/flower_delivery.git
cd flower_delivery
python -m venv venv
source venv/bin/activate  # Для Linux/Mac
venv\Scripts\activate     # Для Windows
pip install -r requirements.txt
python manage.py migrate
python manage.py runserver
