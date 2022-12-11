from dataclasses import dataclass
from series.models import SeriesModel
from typing import Optional


@dataclass
class NewSeries:
    series: SeriesModel
    new_episodes_count: Optional[int] = None
    last_season: Optional[int] = None
    last_episode: Optional[int] = None