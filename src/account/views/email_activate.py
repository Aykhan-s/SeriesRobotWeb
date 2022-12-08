from django.shortcuts import redirect
from django.contrib import messages
from account.models import User
from django.contrib.auth.tokens import default_token_generator
from django.utils.http import urlsafe_base64_decode


def activate_view(request, uidb64, token):
    try:
        uid = urlsafe_base64_decode(uidb64).decode()
        user = User._default_manager.get(pk=uid)
    except(TypeError, ValueError, OverflowError, User.DoesNotExist):
        user = None
    if user is not None and default_token_generator.check_token(user, token):
        user.email_is_verified = True
        user.save()
        messages.success(request, "Thank you for your email confirmation. You will receive notifications of new episodes. ")
        return redirect('homepage')
    else:
        messages.info(request, "Activation link is invalid!")
        return redirect('profile-editing')