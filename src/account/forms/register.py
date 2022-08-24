from django.contrib.auth.forms import UserCreationForm
from account.models import User


class RegisterForm(UserCreationForm):
    password = None

    class Meta:
        model = User
        fields = ('username',
                'email',
                'password1',
                'password2',
                'imdb_api_key')
