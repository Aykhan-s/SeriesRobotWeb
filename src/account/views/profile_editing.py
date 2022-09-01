from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from account.forms import ProfileEditingForm
from requests import get


@login_required(login_url='/')
def profile_editing_view(request):
    if request.method == 'POST':
        form = ProfileEditingForm(request.POST, instance=request.user)
        if form.is_valid():
            raw_data = get(f"https://imdb-api.com/en/API/Title/{request.POST['imdb_api_key']}/tt0110413")

            if raw_data.status_code != 200:
                messages.info(request, 'Account not created. Please try again later')
                return redirect('profile-editing')
            data = raw_data.json()

            if data['errorMessage']:
                if 'Maximum usage' in data['errorMessage']:
                    messages.info(request, f"IMDB API: {data['errorMessage']}")
                    return redirect('profile-editing')

                elif data['errorMessage'] == 'Invalid API Key':
                    form.add_error('imdb_api_key', 'Invalid API Key')
                    return render(request, 'profile_editing.html', context={"form": form})
                messages.info(request, f"IMDB API: {data['errorMessage']}")
                return redirect('profile-editing')

            form.save()
            messages.success(request, 'Profile Updated')
            return redirect('homepage')

    else:
        form = ProfileEditingForm(instance=request.user)

    return render(request, 'profile_editing.html', context={"form": form})
