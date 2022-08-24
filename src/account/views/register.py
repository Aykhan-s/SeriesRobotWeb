from django.shortcuts import render, redirect
from django.contrib import messages
from account.forms import RegisterForm
from django.contrib.auth import login, authenticate 
from django.core.exceptions import ValidationError
from requests import get


def register_view(request):
    if request.method == 'POST':
        form = RegisterForm(request.POST)
        if form.is_valid():
            # raw_data = get(f"https://imdb-api.com/en/API/Title/{request.POST['imdb_api_key']}/tt0110413")
            # if raw_data.status_code == 200: data = raw_data.json()
            # else: 
            #     messages.info(request, 'Account not created. Please try again later')
            #     return redirect('register')

            # if data['errorMessage'] == 'Invalid API Key':
            #     messages.info(request, 'Invalid API Key')
            #     return redirect('register')

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