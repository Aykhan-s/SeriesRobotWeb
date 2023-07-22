from ._requests import get_request
from datetime import datetime
from .exceptions import *
from .new_series_model import NewSeries
from series.models import SeriesModel
from typing import (List,
                    Dict,
                    Union)


class SeriesCounter:
    def __init__(self, api_key: str) -> None:
        self.api_key = api_key
        self.new_series_list: List[NewSeries] = []
        self.error_series: List[SeriesModel] = []

    def get_episode_count(self, series: SeriesModel, data_seasons: Dict) -> Union[
            StatusCodeError,
            APIError,
            MaximumUsageError,
            Dict
        ]:

        now_date = datetime.strptime(datetime.strftime(datetime.utcnow(),'%d %b %Y'), '%d %b %Y')
        data_return = {
            'new_episodes_count': 0,
            'last_season': series.watched_season,
            'last_episode': series.watched_episode
        }
        seasons = data_seasons['tvSeriesInfo']['seasons']

        for season_number in seasons[seasons.index(str(series.watched_season)):]:
            data_episodes = get_request(f"https://imdb-api.com/en/API/SeasonEpisodes/k_ae700oad/{series.imdb_id}/{season_number}")
            episodes = data_episodes['episodes']

            for episode_number in range(int(series.watched_episode) if season_number == str(series.watched_season) else 0, len(episodes)):
                released_date = episodes[episode_number]['released'].replace('.', '')

                try:
                    episode_date = datetime.strptime(released_date, '%d %b %Y')
                    if (episode_date - now_date).days > 0:
                        raise ValueError

                    data_return['last_season'] = int(season_number)
                    data_return['last_episode'] = episode_number+1
                    data_return['new_episodes_count'] += 1

                except ValueError: return data_return
        return data_return

    def find_new_series(self, series: List[SeriesModel]) -> Union[
            MaximumUsageError,
            InvalidAPIKey,
            None
        ]:
        for s in series:
            try:
                data = get_request(f"https://imdb-api.com/en/API/Title/{self.api_key}/{s.imdb_id}")

            except (StatusCodeError, APIError):
                self.error_series.append(s)

            else:
                try:
                    data = self.get_episode_count(s, data)
                    if data['new_episodes_count'] != s.new_episodes_count:
                        self.new_series_list.append(
                            NewSeries(series=s, **data)
                        )
                except (StatusCodeError, APIError):
                    self.error_series.append(s)

    def find_last_episode(self, series: SeriesModel) -> Union[
            MaximumUsageError,
            StatusCodeError,
            InvalidAPIKey,
            APIError,
            NewSeries
        ]:

        data = get_request(f"https://imdb-api.com/en/API/Title/{self.api_key}/{series.imdb_id}")
        data = self.get_episode_count(series, data)
        return NewSeries(series=series, **data)