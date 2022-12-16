from dataclasses import dataclass
from series.models import SeriesModel
from typing import Optional


@dataclass
class NewSeries:
    series: SeriesModel
    new_episodes_count: int
    last_season: int
    last_episode: int