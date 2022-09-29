import os
from celery import Celery


os.environ.setdefault("DJANGO_SETTINGS_MODULE", "config.settings.development")
app = Celery("django_celery")
app.config_from_object("django.conf:settings", namespace="CELERY")
app.autodiscover_tasks()

app.conf.beat_schedule = {
    'send-emails': {
        'task': 'send_emails',
        'schedule': 86400,
    },
}  