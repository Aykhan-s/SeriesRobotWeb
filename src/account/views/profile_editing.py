from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from account.forms import ProfileEditingForm


@login_required(login_url='/')
def profile_editing_view(request):
    if request.method == 'POST':
        form = ProfileEditingForm(request.POST, instance=request.user)
        if form.is_valid():
            form.save()

            messages.success(request, 'Profile Updated')
            return redirect('homepage')

    else:
        form = ProfileEditingForm(instance=request.user)

    return render(request, 'profile_editing.html', context={"form": form})
