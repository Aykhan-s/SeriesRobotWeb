from django.db import models
from django.contrib.auth.models import AbstractUser
from API_client import APIClient
from django.core.exceptions import ValidationError


class User(AbstractUser):
    imdb_api_key = models.CharField(max_length=15, blank=False, null=False)

    def clean(self) -> None:
        client = APIClient(self.imdb_api_key)
        client.key_control()
        # raw_data = get(f"https://imdb-api.com/en/API/Title/{self.imdb_api_key}/tt0110413")

        # if raw_data.status_code == 200: data = raw_data.json()
        # else: raise ValidationError('Account not created. Please try again later')
        # if not data['errorMessage']: raise ValidationError(data['errorMessage'])

    class Meta:
        db_table = 'user'
        verbose_name = 'User'
        verbose_name_plural = 'Users'

    def __str__(self):
        return self.username