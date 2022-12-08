from django.shortcuts import (render,
                            redirect)
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from account.forms import ProfileEditingForm
from requests import get
from .send_otp import send_otp_view


@login_required(login_url='/')
def profile_editing_view(request):
    if request.method == 'POST':
        form = ProfileEditingForm(request.POST, instance=request.user)
        if form.is_valid():
            if 'imdb_api_key' in form.changed_data:
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

            if 'email' in form.changed_data:
                to_email = form.cleaned_data.get('email')
                if to_email is not None:
                    if form.cleaned_data.get('send_email'):
                        form.add_error('send_email', 'You must verify the email before enabling the send email feature')
                        return render(request, 'profile_editing.html', context={"form": form})
                    user = request.user
                    user.email_is_verified = False
                    form.save()
                    user.save()
                    return send_otp_view(request=request)

                elif 'send_email' in form.changed_data and form.cleaned_data.get('send_email'):
                    form.add_error('send_email', 'Email field is required to receive email notifications')
                    return render(request, 'profile_editing.html', context={"form": form})

                user = request.user
                user.email_is_verified = False
                user.send_email = False
                form.save()
                user.save()
                messages.success(request, 'Profile Updated')
                return redirect('homepage')

            elif form.cleaned_data.get('send_email'):
                if form.cleaned_data.get('email') is None:
                    form.add_error('send_email', 'Email field is required to receive email notifications.')
                    return render(request, 'profile_editing.html', context={"form": form})

                elif not request.user.email_is_verified:
                    form.add_error('send_email', 'You must first verify the email.')
                    return render(request, 'profile_editing.html', context={"form": form})

            form.save()
            messages.success(request, 'Profile Updated')
            return redirect('homepage')

    else:
        form = ProfileEditingForm(instance=request.user)

    return render(request, 'profile_editing.html', context={"form": form})
