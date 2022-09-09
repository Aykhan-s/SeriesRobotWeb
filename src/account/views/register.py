from django.shortcuts import (render,
                            redirect)
from django.contrib import messages
from account.forms import RegisterForm
from django.contrib.auth import (login,
                                authenticate)
from requests import get
from account.models import User
from django.contrib.auth.tokens import default_token_generator
from django.contrib.sites.shortcuts import get_current_site
from django.core.mail import EmailMessage
from django.shortcuts import render
from django.template.loader import render_to_string
from django.utils.encoding import force_bytes
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode


def register_view(request):
    if request.method == 'POST':
        form = RegisterForm(request.POST)
        if form.is_valid():
            raw_data = get(f"https://imdb-api.com/en/API/Title/{request.POST['imdb_api_key']}/tt0110413")

            if raw_data.status_code != 200:
                messages.info(request, 'Account not created. Please try again later')
                return redirect('register')
            data = raw_data.json()

            if data['errorMessage']:
                if 'Maximum usage' in data['errorMessage']:
                    messages.info(request, f"IMDB API: {data['errorMessage']}")
                    return redirect('register')

                elif data['errorMessage'] == 'Invalid API Key':
                    form.add_error('imdb_api_key', 'Invalid API Key')
                    return render(request, 'register.html', context={"form": form})
                messages.info(request, f"IMDB API: {data['errorMessage']}")
                return redirect('register')

            to_email = form.cleaned_data.get('email')
            form.save()
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password1')
            user = authenticate(username=username, password=password)
            login(request, user)
            if to_email is not None:
                current_site = get_current_site(request)
                mail_subject = 'Activate your account.'
                message = render_to_string('acc_active_email.html', {
                    'user': user,
                    'domain': current_site.domain,
                    'uid': urlsafe_base64_encode(force_bytes(user.pk)),
                    'token': default_token_generator.make_token(user),
                })
                email = EmailMessage(
                    mail_subject, message, to=[to_email]
                )
                email.send()
                messages.warning(request, "Please confirm your email address to receive notifications of new episodes.")
                return redirect('homepage')

            messages.success(request, 'Registration Successful')
            return redirect('homepage')

    else: 
        form = RegisterForm()

    return render(request, 'register.html', context={"form": form})


def activate_view(request, uidb64, token):
    try:
        uid = urlsafe_base64_decode(uidb64).decode()
        user = User._default_manager.get(pk=uid)
    except(TypeError, ValueError, OverflowError, User.DoesNotExist):
        user = None
    if user is not None and default_token_generator.check_token(user, token):
        user.email_notification_is_active = True
        user.save()
        messages.success(request, "Thank you for your email confirmation. You will receive notifications of new episodes. ")
        return redirect('homepage')
    else:
        messages.info(request, "Activation link is invalid!")
        return redirect('register')