from django.shortcuts import redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from account.models import User
from imdb_api_access import SeriesCounter
from imdb_api_access import (
    MaximumUsageError,
    InvalidAPIKey
)


@login_required(login_url='/account/login')
def new_episodes_view(request):
    series = User.objects.get(id=request.user.id).series.filter(show=True).order_by('-id')

    series_counter = SeriesCounter(request.user.imdb_api_key)

    try:
        series_counter.find_new_series(series)
        series_len = len(series_counter.new_series_list)
        error_series_len = len(series_counter.error_series)

    except MaximumUsageError as e:
        if series_len := len(series_counter.new_series_list):
            for updated_series in series_counter.new_series_list:
                updated_series.series.last_season = updated_series.last_season
                updated_series.series.last_episode = updated_series.last_episode
                updated_series.series.new_episodes_count = updated_series.new_episodes_count
                updated_series.save()
            messages.warning(request,
                f"{series_len} series updated (some series could not be updated). {str(e)}")
            return redirect('homepage')

        messages.warning(request,
            f"Series could not be updated. {str(e)}")
        return redirect('homepage')

    except InvalidAPIKey as e:
        messages.info(request,
            f"Series could not be updated: {str(e.message)}")
        return redirect('homepage')

    if series_len:
        for updated_series in series_counter.new_series_list:
            updated_series.series.last_season = updated_series.last_season
            updated_series.series.last_episode = updated_series.last_episode
            updated_series.series.new_episodes_count = updated_series.new_episodes_count
            updated_series.series.save()

        if error_series_len:
            messages.warning(request,
                f"{series_len} series updated ({error_series_len} series could not be updated).")
            return redirect('homepage')

        messages.warning(request,
            f"{series_len} series updated.")
        return redirect('homepage')

    if error_series_len:
        messages.warning(request,
            f"{error_series_len} series could not be updated.")
        return redirect('homepage')

    messages.warning(request, "0 series updated")
    return redirect('homepage')