from celery import shared_task
from account.models import User
from django.template.loader import render_to_string
from imdb_api_access import SeriesCounter
from imdb_api_access import MaximumUsageError
from django.core.mail import (EmailMessage,
                            get_connection)
# from celery.utils.log import get_task_logger


# logger = get_task_logger(__name__)

def update_series(updated_series):
    updated_series.series.last_season = updated_series.last_season
    updated_series.series.last_episode = updated_series.last_episode
    updated_series.series.new_episodes_count = updated_series.new_episodes_count

def compose_email(user):
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
            return render_to_string(
                'email/maximum_usage_notification.html',
                {
                    'user': user,
                    'new_series_list': series_counter.new_series_list,
                    'maximum_usage': str(e),
                },
            )
        return

    if series_len:
        for updated_series in series_counter.new_series_list:
            update_series(updated_series)
            updated_series.series.save()

        if series_counter.error_series:
            return render_to_string('email/error_series_notification.html', {
                'user': user,
                'new_series_list': series_counter.new_series_list,
                'error_series_list': series_counter.error_series,
            })

        return render_to_string('email/new_series_notification.html', {
            'user': user,
            'new_series_list': series_counter.new_series_list,
        })

@shared_task(name='send_emails')
def send_feedback_email_task():
    users = User.objects.filter(send_email=True)

    with get_connection() as connection:
        for user in users:
            if html_message := compose_email(user):
                msg = EmailMessage(
                        subject='Series Updated!',
                        body=html_message,
                        from_email='series.notification@gmail.com',
                        to=[user.email],
                        connection=connection,
                    )
                msg.content_subtype = 'html'
                msg.send()