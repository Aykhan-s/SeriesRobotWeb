from celery import shared_task
from account.models import User
from requests import get
from datetime import datetime
from django.template.loader import render_to_string
from django.core.mail import EmailMessage
from celery.utils.log import get_task_logger


logger = get_task_logger(__name__)

def get_request(link):
    raw_data = get(link)

    if raw_data.status_code == 200:
        data = raw_data.json()
        if not data['errorMessage']:
            return data
        logger.info(f"error message: {data['errorMessage']}\nlink: {link}")
        return None
    logger.info(f"status code: {raw_data.status_code}\nlink: {link}")

def episode_counter(imdb_api_key, s, data):
    now_date = datetime.strptime(datetime.strftime(datetime.utcnow(),'%d %b %Y'), '%d %b %Y')
    new_episodes_count = 0

    for n in data['tvSeriesInfo']['seasons'][data['tvSeriesInfo']['seasons'].index(str(s.last_season)):]:
        data = get_request(f"https://imdb-api.com/en/API/SeasonEpisodes/{imdb_api_key}/{s.imdb_id}/{n}")
        if data is None: return None

        episodes = data['episodes']
        for i in range(int(s.last_episode) if n == str(s.last_season) else 0, len(episodes)):
            released_date = episodes[i]['released'].replace('.', '')
            try:
                episode_date = datetime.strptime(released_date, '%d %b %Y')
                if (episode_date - now_date).days > 0:
                    raise ValueError
            except ValueError:
                try:
                    return new_episodes_count, int(last_n)+1, last_i+1 if new_episodes_count > 0 else 0, 0, 0
                except UnboundLocalError:
                    return new_episodes_count, int(n), last_i+1 if new_episodes_count > 0 else 0, 0, 0
            last_i = i
            new_episodes_count += 1
        last_n = n

    return new_episodes_count, n, i+1 if new_episodes_count > 0 else 0, 0, 0

@shared_task(name='send_emails')
def send_feedback_email_task():
    users = User.objects.filter(email_is_verified=True)
    for user in users:
        series = user.series.filter(show=True).order_by('-id')
        series_new_episodes = []

        for s in series:
            data = get_request(f"https://imdb-api.com/en/API/Title/{user.imdb_api_key}/{s.imdb_id}")

            if data is None:
                series_new_episodes = []
                break
            data = episode_counter(user.imdb_api_key, s, data)
            if data is None:
                series_new_episodes = []
                break

            if data[0]:
                series_new_episodes.append([s,
                    {'count': data[0],
                    'last_season': data[1],
                    'last_episode': data[2]}
                    ])

        if series_new_episodes:
            message = render_to_string('new_episodes_verification.html', {
                'user': user,
                'data': series_new_episodes
            })
            email = EmailMessage(
                'New Episodes!', message, to=[user.email]
            )
            email.send()