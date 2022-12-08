from django.shortcuts import (render,
                            redirect)
from django.contrib import messages
from account.forms import RegisterForm
from django.contrib.auth import (login,
                                authenticate)
from requests import get
from django.shortcuts import render
from .send_otp import send_otp_view


def register_view(request):  # sourcery skip: extract-method
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
            if to_email is None and form.cleaned_data.get('send_email'):
                form.add_error('send_email', 'Email field is required to receive email notifications.')
                return render(request, 'register.html', context={"form": form})

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