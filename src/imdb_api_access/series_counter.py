from ._requests import get_request
from datetime import datetime
from .exceptions import *
from .new_series_model import NewSeries
from series.models import SeriesModel
from typing import (List,
                    Tuple,
                    Dict,
                    Union)


class SeriesCounter:
    def __init__(self, api_key: str) -> None:
        self.api_key = api_key
        self.new_series_list: List[NewSeries] = []
        self.error_series: List[SeriesModel] = []

    def get_episode_count(self, series: SeriesModel, data: Dict) -> Union[StatusCodeError, APIError, MaximumUsageError, Tuple]:
        # sourcery skip: aware-datetime-for-utc
        now_date = datetime.strptime(datetime.strftime(datetime.utcnow(),'%d %b %Y'), '%d %b %Y')
        new_episodes_count = 0

        for n in data['tvSeriesInfo']['seasons'][data['tvSeriesInfo']['seasons'].index(str(series.last_season)):]:
            data = get_request(f"https://imdb-api.com/en/API/SeasonEpisodes/{self.api_key}/{series.imdb_id}/{n}")

            episodes = data['episodes']
            for i in range(int(series.last_episode) if n == str(series.last_season) else 0, len(episodes)):
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

    def find_new_series(self, series: List[NewSeries]) -> Union[MaximumUsageError, None]:
        for s in series:
            try:
                data = get_request(f"https://imdb-api.com/en/API/Title/{self.api_key}/{s.imdb_id}")

            except (StatusCodeError, APIError):
                self.error_series.append(s)

            else:
                data = self.get_episode_count(s, data)
                if data[0]:
                    self.new_series_list.append(
                        NewSeries(
                            series=s,
                            new_episodes_count=data[0],
                            last_season=data[1],
                            last_episode=data[2]
                        )
                    )