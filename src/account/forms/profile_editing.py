from django.contrib.auth.forms import UserChangeForm
from account.models import User


class ProfileEditingForm(UserChangeForm):
    password = None

    class Meta:
        model = User
        fields = ('email', 'username', 'imdb_api_key')