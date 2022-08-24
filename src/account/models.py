from django.db import models
from django.contrib.auth.models import AbstractUser


class User(AbstractUser):
    imdb_api_key = models.CharField(max_length=15, blank=False, null=False)

    class Meta:
        db_table = 'user'
        verbose_name = 'User'
        verbose_name_plural = 'Users'

    def __str__(self):
        return self.username