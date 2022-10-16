from .base import *


DEBUG = True

ALLOWED_HOSTS = ['*']

CSRF_TRUSTED_ORIGINS=['http://127.0.0.1:8000']

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': BASE_DIR / 'db.sqlite3',
    }
}

STATIC_URL = '/static/'

# STATIC_ROOT = os.path.join(BASE_DIR, 'static')
STATICFILES_DIRS = [
    BASE_DIR / 'static'
]