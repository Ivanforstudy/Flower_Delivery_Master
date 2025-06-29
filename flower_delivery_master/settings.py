from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent

SECRET_KEY = '#q4!w-b6(dv0p@6*g1!uu$8(sf)6=y$9(rtu2rz)kzv$ym+$il'

DEBUG = True

ALLOWED_HOSTS = ['127.0.0.1', 'localhost']

# Приложения
INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',

    # Приложения проекта
    'main',
    'accounts',
    'orders',
    'reviews',
    'analytics',
    'telegram_bot',
    'catalog',
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'flower_delivery_master.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [BASE_DIR / 'templates'],  # Глобальные шаблоны, если будут
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',  # Нужно для messages и login
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
            ],
        },
    },
]

WSGI_APPLICATION = 'flower_delivery_master.wsgi.application'


# База данных
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': BASE_DIR / 'db.sqlite3',
    }
}


# Локализация
LANGUAGE_CODE = 'ru-ru'
TIME_ZONE = 'Europe/Moscow'
USE_I18N = True
USE_L10N = True
USE_TZ = True


# Статика
STATIC_URL = '/static/'
STATICFILES_DIRS = [BASE_DIR / 'static']  # Для разработки
STATIC_ROOT = BASE_DIR / 'staticfiles'    # Для продакшена (collectstatic)

# Медиа
MEDIA_URL = '/media/'
MEDIA_ROOT = BASE_DIR / 'media'


# Пользовательская модель
AUTH_USER_MODEL = 'accounts.CustomUser'


# Перенаправления после логина/логаута
LOGIN_REDIRECT_URL = '/'
LOGOUT_REDIRECT_URL = '/accounts/login/'


# Телеграм-бот
TELEGRAM_BOT_TOKEN = '7763598812:AAHa-yOc3rZ0wINeAptiE6ktRflzADi_OqU'

# Настройка автоидентификаторов
DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'
