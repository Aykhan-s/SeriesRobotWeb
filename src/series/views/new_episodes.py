from django.shortcuts import (render,
                            redirect)
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from account.models import User
from requests import get
from datetime import datetime
from django.core.paginator import Paginator


def get_request(request, link):
    raw_data = get(link)

    if raw_data.status_code != 200:
        messages.info(request, "Can't search for TV Series. Please try again.")
        return redirect('homepage')
    data = raw_data.json()

    if data['errorMessage']:
        messages.info(request, f"IMDB API: {data['errorMessage']}")
        return redirect('homepage')
    return data

def episode_counter(request, s, data):
    now_date = datetime.strptime(datetime.strftime(datetime.utcnow(),'%d %b %Y'), '%d %b %Y')
    new_episodes_count = 0

    for n in data['tvSeriesInfo']['seasons'][data['tvSeriesInfo']['seasons'].index(str(s.last_season)):]:
        data = get_request(request, f"https://imdb-api.com/en/API/SeasonEpisodes/{request.user.imdb_api_key}/{s.imdb_id}/{n}")
        if type(data) is not dict: return data

        episodes = data['episodes']
        for i in range(int(s.last_episode) if n == str(s.last_season) else 0, len(episodes)):
            released_date = episodes[i]['released'].replace('.', '')
            try:
                episode_date = datetime.strptime(released_date, '%d %b %Y')
                if (episode_date - now_date).days > 0:
                    raise ValueError
            except ValueError: return new_episodes_count, last_n, last_i+1
            last_i = i
            new_episodes_count += 1
        last_n = n

    return new_episodes_count, n, i+1

@login_required(login_url='/account/login')
def new_episodes_view(request):
    series = User.objects.get(id=request.user.id).series.filter(show=True).order_by('-id')
    series_new_episodes = []

    for s in series:
        data = get_request(request, f"https://imdb-api.com/en/API/Title/{request.user.imdb_api_key}/{s.imdb_id}")
        if type(data) is not dict: return data
        data = episode_counter(request, s, data)
        if type(data) is not tuple: return data
        if data[0]:
            series_new_episodes.append([s,
                {'count': data[0],
                'last_season': data[1],
                'last_episode': data[2]}
                ])

    if series_new_episodes:
        page = request.GET.get('page')
        paginator = Paginator(series_new_episodes, 1)
        return render(request, 'new_episodes.html', context={'data': paginator.get_page(page)})
    messages.warning(request, "There are no new episodes of any series :(")
    return redirect('homepage')