from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent

# Включаем режим отладки для разработки
DEBUG = True

# Пока разрешаем все хосты, чтобы избежать ошибок. В продакшене обязательно указать реальные домены.
ALLOWED_HOSTS = []

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',

    'catalog',
    'orders',
    'users',
    'reviews',
    'analytics',
]

AUTH_USER_MODEL = 'users.CustomUser'

# Настройки медиафайлов
MEDIA_URL = '/media/'
MEDIA_ROOT = BASE_DIR / 'media'

# Настройки статики
STATIC_URL = '/static/'
STATICFILES_DIRS = [BASE_DIR / 'static']
STATIC_ROOT = BASE_DIR / 'staticfiles'

LOGIN_REDIRECT_URL = '/'
LOGOUT_REDIRECT_URL = '/'
