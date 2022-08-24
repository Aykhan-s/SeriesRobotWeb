from django.contrib.auth import logout
from django.shortcuts import redirect
from django.contrib import messages
from django.contrib.auth.decorators import login_required


@login_required(login_url='/account/login')
def logout_view(request):
    logout(request)

    messages.success(request, 'Logged Out')
    return redirect('login')
