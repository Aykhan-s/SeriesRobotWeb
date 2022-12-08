from django.contrib.auth.decorators import login_required
from django.contrib.sites.shortcuts import get_current_site
from django.template.loader import render_to_string
from django.utils.http import urlsafe_base64_encode
from django.utils.encoding import force_bytes
from django.contrib.auth.tokens import default_token_generator
from django.core.mail import EmailMessage
from django.contrib import messages
from django.shortcuts import redirect
from django.views.decorators.http import require_http_methods
from django_ratelimit.decorators import ratelimit


@ratelimit(key='user', rate='1/125s', block=False)
@login_required(login_url='/')
@require_http_methods(['GET', 'POST'])
def send_otp_view(request):
    if getattr(request, 'limited', False):
        messages.warning(request, 'You can only get 1 verification code every 2 minutes.')
        return redirect('homepage')

    user = request.user
    if user.email is None:
        messages.warning(request, 'you must add your email first')
        return redirect('profile-editing')

    if user.email_is_verified:
        messages.warning(request, 'your email account is already verified')
        return redirect('homepage')

    current_site = get_current_site(request)
    mail_subject = 'Activate your account.'
    message = render_to_string('acc_active_email.html', {
        'user': user,
        'domain': current_site.domain,
        'uid': urlsafe_base64_encode(force_bytes(user.pk)),
        'token': default_token_generator.make_token(user),
    })
    email = EmailMessage(
        mail_subject, message, to=[user.email]
    )
    email.send()

    messages.warning(request, f"Verification message sent to {user.email}.")
    return redirect('homepage')