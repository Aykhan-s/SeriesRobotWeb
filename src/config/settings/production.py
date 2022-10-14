from .base import *


DEBUG = True

ALLOWED_HOSTS = ['www.series-notification.online', 'www.series-notification.online', '130.61.19.69']

# CSRF_TRUSTED_ORIGINS=['http://127.0.0.1:80']

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql_psycopg2',
        'NAME': env('DB_NAME'),
        'USER': env('DB_USER'),
        'PASSWORD': env('DB_PASSWORD'),
        'HOST': 'db',
        'PORT': '5432',
    }
}

STATIC_URL = '/django_static/'
STATIC_ROOT = os.path.join(os.path.dirname(os.path.dirname(BASE_DIR)), 'django_static')
STATICFILES_DIRS = [
    BASE_DIR / 'static'
]