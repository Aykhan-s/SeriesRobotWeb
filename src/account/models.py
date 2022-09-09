from django.db import models
from django.contrib.auth.models import AbstractUser


class User(AbstractUser):
    first_name = None
    last_name = None
    email = models.EmailField('email', unique=True, blank=True, null=True)
    imdb_api_key = models.CharField(max_length=15, blank=False, null=False)
    email_notification_is_active = models.BooleanField(default=False)

    class Meta:
        db_table = 'user'
        verbose_name = 'User'
        verbose_name_plural = 'Users'

    def __str__(self):
        return self.username