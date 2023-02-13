from celery import Celery
from celery.schedules import crontab
# import os


# os.environ.setdefault("DJANGO_SETTINGS_MODULE", "config.settings.production")
app = Celery("django_celery")
app.config_from_object("django.conf:settings", namespace="CELERY")
app.autodiscover_tasks()

app.conf.beat_schedule = {
    'send-emails': {
        'task': 'send_emails',
        'schedule': crontab(hour=5, minute=55),
    },
}