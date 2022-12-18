from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import PasswordChangeForm
from django.contrib.auth import update_session_auth_hash
from django.contrib import messages
from django.shortcuts import (render,
                            redirect)


@login_required(login_url='/')
def change_password_view(request):
    if request.method == 'POST':
        form = PasswordChangeForm(request.user, request.POST)
        if form.is_valid():
            user = form.save()
            update_session_auth_hash(request, user)

            messages.success(request, 'Password changed')
            return redirect('homepage')

    else:
        form = PasswordChangeForm(request.user)

    return render(request, 'change_password.html', context={'form': form})