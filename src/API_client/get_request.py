from requests import get
from django.core.exceptions import ValidationError


class APIClient:
    def __init__(self, api_key: str) -> None:
        self.api_key = api_key

    def __get_data(self, link: str) -> dict:
        raw_data = get(link)
        if raw_data.status_code == 200:
            data = raw_data.json()

            if data['errorMessage'] == 'Invalid API Key': raise ValidationError('Invalid API Key')
            elif data['errorMessage']: raise ValidationError('id is not correct.')

            return data
        raise ValidationError('Could not created. Please try again later.')

    def key_control(self) -> None:
        self.__get_data(f"https://imdb-api.com/en/API/Title/{self.api_key}/tt7939766")

    def get_seasons(self, series_id: str) -> list:
        data = self.__get_data(f"https://imdb-api.com/en/API/Title/{self.api_key}/{series_id}")

        if not data['tvSeriesInfo']:
            raise ValidationError('This is not a TV series id')
        return data['tvSeriesInfo']['seasons']

    def get_episodes_count(self, season: int, series_id: str) -> int:
        data = self.__get_data(
            f"https://imdb-api.com/en/API/SeasonEpisodes/{self.api_key}/{series_id}/{season}")
        return len(data['episodes'])