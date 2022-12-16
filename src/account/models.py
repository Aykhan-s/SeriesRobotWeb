from django.db import models
from django.contrib.auth.models import AbstractUser


class User(AbstractUser):
    first_name = None
    last_name = None
    email = models.EmailField('email', null=True, blank=True, unique=True)
    imdb_api_key = models.CharField(max_length=15, blank=False, null=False, unique=True)
    email_is_verified = models.BooleanField(default=False)
    send_email = models.BooleanField(default=False)

    def clean(self):
        if self.email == '':
            self.email = None

    class Meta:
        db_table = 'user'
        verbose_name = 'User'
        verbose_name_plural = 'Users'

    def __str__(self):
        return self.username