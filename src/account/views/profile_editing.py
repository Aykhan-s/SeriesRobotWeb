from django.shortcuts import (render,
                            redirect)
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from account.forms import ProfileEditingForm
from requests import get
from django.contrib.auth.tokens import default_token_generator
from django.contrib.sites.shortcuts import get_current_site
from django.template.loader import render_to_string
from django.utils.encoding import force_bytes
from django.utils.http import urlsafe_base64_encode
from django.core.mail import EmailMessage


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

            form.save()
            if 'email' in form.changed_data:
                user = request.user
                user.email_notification_is_active = False
                user.save()
                to_email = form.cleaned_data.get('email')
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

            messages.success(request, 'Profile Updated')
            return redirect('homepage')

    else:
        form = ProfileEditingForm(instance=request.user)

    return render(request, 'profile_editing.html', context={"form": form})
