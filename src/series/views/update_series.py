from series.models import SeriesModel
from django.views.generic import UpdateView
from django.urls import reverse, reverse_lazy
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib import messages
from django.shortcuts import (get_object_or_404,
                            redirect)
from datetime import datetime
from imdb_api_access._requests import get_request
from imdb_api_access import SeriesCounter
from imdb_api_access.exceptions import *


class UpdateSeriesView(LoginRequiredMixin, UpdateView):
    login_url = reverse_lazy('login')
    template_name = 'update_series.html'
    fields = ('title', 'imdb_id', 'watched_season', 'watched_episode', 'show')

    def get_object(self):
        return get_object_or_404(SeriesModel, slug=self.kwargs.get('slug'), user=self.request.user)

    def get_success_url(self):
        messages.success(self.request, 'Series Updated')
        return reverse('homepage')

    def form_valid(self, form):
        series = form.save(commit=False)
        series.user = self.request.user

        if not {'imdb_id', 'watched_season', 'watched_episode'} & set(form.changed_data):
            series.save()
            form.save_m2m()
            return super().form_valid(form)

        try:
            data = get_request(f"https://imdb-api.com/en/API/Title/{series.user.imdb_api_key}/{series.imdb_id}")
        except StatusCodeError:
            messages.info(self.request, 'TV Series can not added. Please try again.')
            return redirect('update-series', self.kwargs.get('slug'))
        except MaximumUsageError:
            messages.info(self.request, f"IMDB API: {data['errorMessage']}")
            return redirect('update-series', self.kwargs.get('slug'))
        except APIError:
            form.add_error('imdb_id', 'ID is not correct.')
            return self.form_invalid(form)

        if not data['tvSeriesInfo']:
            form.add_error('imdb_id', 'This is not a TV series id.')
            return self.form_invalid(form)
        seasons = data['tvSeriesInfo']['seasons']

        if str(series.watched_season) not in seasons:
            form.add_error('watched_season', 'The season number is not correct.')
            return self.form_invalid(form)

        try:
            data = get_request(f"https://imdb-api.com/en/API/SeasonEpisodes/{series.user.imdb_api_key}/{series.imdb_id}/{series.watched_season}")
        except StatusCodeError:
            messages.info(self.request, 'TV Series can not added. Please try again.')
            return redirect('update-series', self.kwargs.get('slug'))
        except MaximumUsageError:
            messages.info(self.request, f"IMDB API: {data['errorMessage']}")
            return redirect('update-series', self.kwargs.get('slug'))
        except APIError:
            form.add_error('imdb_id', 'ID is not correct.')
            return self.form_invalid(form)

        episodes = data['episodes']
        episodes_count = len(episodes)

        if series.watched_episode > episodes_count:
            form.add_error('watched_episode', 'The episode number is not correct.')
            return self.form_invalid(form)

        released_date = episodes[int(series.watched_episode) - 1]['released'].replace('.', '')
        now_date = datetime.strptime(datetime.strftime(datetime.utcnow(),'%d %b %Y'), '%d %b %Y')

        try:
            last_episode_date = datetime.strptime(released_date, '%d %b %Y')
            if (last_episode_date - now_date).days > 0:
                raise ValueError
        except ValueError:
            form.add_error('watched_episode', 'This episode has not been published yet.')
            return self.form_invalid(form)

        series_counter = SeriesCounter(self.request.user.imdb_api_key)
        try:
            new_series = series_counter.find_last_episode(series)
            series.last_season = new_series.last_season
            series.last_episode = new_series.last_episode
            series.new_episodes_count = new_series.new_episodes_count

        except (StatusCodeError, APIError):
            messages.info(self.request, 'TV Series can not updated. Please try again later.')
            return redirect('update-series', self.kwargs.get('slug'))

        except MaximumUsageError as e:
            messages.info(self.request, str(e))
            return redirect('homepage')

        series.save()
        form.save_m2m()
        return super().form_valid(form)