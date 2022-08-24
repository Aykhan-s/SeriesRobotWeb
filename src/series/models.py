from django.db import models
from django.core.exceptions import ValidationError
from API_client import APIClient
from django.core.validators import (MaxValueValidator,
                                    MinValueValidator,
                                    MinLengthValidator)


class SeriesModel(models.Model):
    user = models.ForeignKey('account.User', on_delete=models.CASCADE, related_name='series')
    title = models.CharField(max_length=35, blank=False, null=False)
    imdb_id = models.CharField(max_length=10, validators=[MinLengthValidator(9)],
                            blank=False, null=False)
    last_season = models.IntegerField(validators=[
            MaxValueValidator(30),
            MinValueValidator(1)
        ], blank=False, null=False)
    last_episode = models.IntegerField(validators=[
            MaxValueValidator(60),
            MinValueValidator(1)
        ], blank=False, null=False)
    show = models.BooleanField(default=True)

    def clean(self) -> None:
        if len(self.imdb_id) < 9:
            raise ValidationError(f'Ensure this value has at least 9 characters (it has {len(self.imdb_id)}).')

        if len(self.imdb_id) > 10:
            raise ValidationError(f'Make sure this value is no more than 10 characters (it has {len(self.imdb_id)}).')

        client = APIClient(self.user.imdb_api_key)

        seasons = client.get_seasons(self.imdb_id)
        if str(self.last_season) not in seasons:
            raise ValidationError('The season number you entered is not correct.')

        episodes_count = client.get_episodes_count(self.last_season, self.imdb_id)
        if self.last_episode > episodes_count:
            raise ValidationError('The episode number you entered is not correct.')

    def __str__(self) -> str:
        return f"{self.user.username} - {self.title}"