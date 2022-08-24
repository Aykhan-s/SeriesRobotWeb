from django.shortcuts import render, redirect
from django.contrib import messages
from account.forms import RegisterForm
from django.contrib.auth import login, authenticate 
from requests import get


def register_view(request):
    if request.method == 'POST':
        form = RegisterForm(request.POST)
        if form.is_valid():
            raw_data = get(f"https://imdb-api.com/en/API/Title/{request.POST['imdb_api_key']}/tt0110413")

            if raw_data.status_code != 200:
                messages.info(request, 'Account not created. Please try again later')
                return redirect('register')
            data = raw_data.json()

            if data['errorMessage'] == 'Invalid API Key':
                form.add_error('imdb_api_key', 'Invalid API Key')
                return render(request, 'register.html', context={"form": form})

            form.save()
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password1')
            user = authenticate(username=username, password=password)
            login(request, user)

            messages.success(request, 'Registration Successful')
            return redirect('homepage')

    else:
        form = RegisterForm()

    return render(request, 'register.html', context={"form": form})