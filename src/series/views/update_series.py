from series.models import SeriesModel
from django.views.generic import UpdateView
from django.urls import reverse, reverse_lazy
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib import messages
from django.shortcuts import (get_object_or_404,
                            redirect)
from requests import get
from datetime import datetime


class UpdateSeriesView(LoginRequiredMixin, UpdateView):
    login_url = reverse_lazy('login')
    template_name = 'update_series.html'
    fields = ('title', 'imdb_id', 'last_season', 'last_episode', 'show')

    def get_object(self):
        return get_object_or_404(SeriesModel, slug=self.kwargs.get('slug'), user=self.request.user)

    def get_success_url(self):
        messages.success(self.request, 'Series Updated')
        return reverse('homepage')

    def form_valid(self, form):
        series = form.save(commit=False)
        series.user = self.request.user

        if not {'imdb_id', 'last_season', 'last_episode'} & set(form.changed_data):
            series.save()
            form.save_m2m()
            return super().form_valid(form)

        raw_data = get(f"https://imdb-api.com/en/API/Title/{series.user.imdb_api_key}/{series.imdb_id}")

        if raw_data.status_code != 200:
            messages.info(self.request, 'TV Series can not updated. Please try again.')
            return redirect('update-series', self.kwargs.get('slug'))
        data = raw_data.json()

        if data['errorMessage']:
            if 'Maximum usage' in data['errorMessage']:
                messages.info(self.request, f"IMDB Key: {data['errorMessage']}")
                return redirect("update-series", self.kwargs.get('slug'))
            form.add_error('imdb_id', 'ID is not correct.')
            return self.form_invalid(form)

        if not data['tvSeriesInfo']:
            form.add_error('imdb_id', 'This is not a TV series id.')
            return self.form_invalid(form)
        seasons = data['tvSeriesInfo']['seasons']

        if str(series.last_season) not in seasons:
            form.add_error('last_season', 'The season number is not correct.')
            return self.form_invalid(form)

        raw_data = get(f"https://imdb-api.com/en/API/SeasonEpisodes/{series.user.imdb_api_key}/{series.imdb_id}/{series.last_season}")
        if raw_data.status_code != 200:
            messages.info(self.request, 'TV Series can not added. Please try again.')
            return redirect('update-series', self.kwargs.get('slug'))
        data = raw_data.json()

        if data['errorMessage']:
            if 'Maximum usage' in data['errorMessage']:
                messages.info(self.request, f"IMDB API: {data['errorMessage']}")
                return redirect('update-series', self.kwargs.get('slug'))
            form.add_error('imdb_id', 'ID is not correct.')
            return self.form_invalid(form)
        episodes = data['episodes']

        episodes_count = len(episodes)
        if series.last_episode > episodes_count:
            form.add_error('last_episode', 'The episode number is not correct.')
            return self.form_invalid(form)

        released_date = episodes[int(series.last_episode) - 1]['released'].replace('.', '')
        now_date = datetime.strptime(datetime.strftime(datetime.utcnow(),'%d %b %Y'), '%d %b %Y')
        try:
            last_episode_date = datetime.strptime(released_date, '%d %b %Y')
            if (last_episode_date - now_date).days > 0:
                raise ValueError
        except ValueError:
            form.add_error('last_episode', 'This episode has not been published yet.')
            return self.form_invalid(form)

        series.save()
        form.save_m2m()
        return super().form_valid(form)