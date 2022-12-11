from django.shortcuts import (render,
                            redirect)
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from account.models import User
from imdb_api_access import SeriesCounter
from imdb_api_access import MaximumUsageError


@login_required(login_url='/account/login')
def new_episodes_view(request):
    series = User.objects.get(id=request.user.id).series.filter(show=True).order_by('-id')

    series_counter = SeriesCounter(request.user.imdb_api_key)
    try:
        series_counter.find_new_series(series)
    except MaximumUsageError as e: ...
        # messages.warning(request, f"{e} (some series could not be updated)")

    if series_counter.new_series_list:
        return render(request, 'new_episodes.html', context={'data': series_counter.new_series_list})
    messages.warning(request, "There are no new episodes of any series :(")
    return redirect('homepage')