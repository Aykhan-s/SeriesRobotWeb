from django.db import models
from autoslug import AutoSlugField
from django.core.validators import (MaxValueValidator,
                                    MinValueValidator,
                                    MinLengthValidator)


class SeriesModel(models.Model):
    user = models.ForeignKey('account.User', on_delete=models.CASCADE, related_name='series')
    title = models.CharField(max_length=35, blank=False, null=False)
    imdb_id = models.CharField(max_length=10, validators=[MinLengthValidator(9)],
                            blank=False, null=False)
    watched_season = models.IntegerField(validators=[
            MaxValueValidator(30),
            MinValueValidator(1)
        ], blank=False, null=False)
    watched_episode = models.IntegerField(validators=[
            MaxValueValidator(60),
            MinValueValidator(1)
        ], blank=False, null=False)
    last_season = models.IntegerField(validators=[
            MaxValueValidator(30),
            MinValueValidator(1)],
            default=1)
    last_episode = models.IntegerField(validators=[
            MaxValueValidator(60),
            MinValueValidator(1)],
            default=1)
    new_episodes_count = models.IntegerField(validators=[
            MaxValueValidator(200),
            MinValueValidator(0)],
            default=0)
    show = models.BooleanField(default=True)
    slug = AutoSlugField(populate_from='title', unique=True)

    def __str__(self) -> str:
        return f"{self.user.username} - {self.title}"