from celery import shared_task
from account.models import User
from requests import get
from datetime import datetime
from django.template.loader import render_to_string
from django.core.mail import EmailMessage
from celery.utils.log import get_task_logger
from imdb_api_access import SeriesCounter
from imdb_api_access import MaximumUsageError


# logger = get_task_logger(__name__)


def update_series(updated_series):
    updated_series.series.last_season = updated_series.last_season
    updated_series.series.last_episode = updated_series.last_episode
    updated_series.series.new_episodes_count = updated_series.new_episodes_count

def send_email(user):
    series = user.series.filter(show=True).order_by('-id')

    series_counter = SeriesCounter(user.imdb_api_key)
    try:
        series_counter.find_new_series(series)
        series_len = len(series_counter.new_series_list)
    except MaximumUsageError as e:
        if series_len := len(series_counter.new_series_list):
            for updated_series in series_counter.new_series_list:
                update_series(updated_series)
                updated_series.save()
            message = render_to_string('new_episodes_notification.html', {
                'user': user,
                'new_series_list': series_counter.new_series_list,
                'error_series_list': series_counter.error_series,
                'maximum_usage': str(e)
            })
            email = EmailMessage(
                'New Episodes!', message, to=[user.email]
            )
            email.send()
            return
        return

    if series_len:
        for updated_series in series_counter.new_series_list:
            update_series(updated_series)
            updated_series.series.save()

        message = render_to_string('new_episodes_notification.html', {
            'user': user,
            'new_series_list': series_counter.new_series_list,
            'error_series_list': series_counter.error_series,
            'maximum_usage': ''
        })
        email = EmailMessage(
            'New Episodes!', message, to=[user.email]
        )
        email.send()
        return

@shared_task(name='send_emails')
def send_feedback_email_task():
    users = User.objects.filter(send_email=True)
    for user in users: send_email(user)