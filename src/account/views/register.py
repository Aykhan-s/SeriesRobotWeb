from django.shortcuts import (render,
                            redirect)
from django.contrib import messages
from account.forms import RegisterForm
from django.contrib.auth import (login,
                                authenticate)
from imdb_api_access._requests import get_request
from imdb_api_access.exceptions import *
from django.shortcuts import render
from .send_otp import send_otp_view


def register_view(request):  # sourcery skip: extract-method
    if request.method == 'POST':
        form = RegisterForm(request.POST)
        if form.is_valid():
            try:
                get_request(f"https://imdb-api.com/en/API/Title/{request.POST['imdb_api_key']}/tt0110413")

            except StatusCodeError:
                messages.info(request, 'Account not created. Please try again later')
                return redirect('register')

            except MaximumUsageError as e:
                messages.info(request, str(e))
                return redirect('register')

            except (APIError, InvalidAPIKey) as e:
                if e.message == 'Invalid API Key':
                    form.add_error('imdb_api_key', 'Invalid API Key')
                    return render(request, 'register.html', context={"form": form})

                messages.info(request, str(e))
                return redirect('register')

            to_email = form.cleaned_data.get('email')

            form.save()
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password1')
            user = authenticate(username=username, password=password)
            login(request, user)
            if to_email is not None:
                return send_otp_view(request=request)

            messages.success(request, 'Registration Successful')
            return redirect('homepage')

    else: 
        form = RegisterForm()

    return render(request, 'register.html', context={"form": form})