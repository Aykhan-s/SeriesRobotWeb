from django.views.generic import DetailView
from account.models import User
from django.urls import reverse_lazy
from django.shortcuts import get_object_or_404
from django.contrib.auth.mixins import LoginRequiredMixin


class ProfileDetailView(LoginRequiredMixin, DetailView):
    login_url = reverse_lazy('login')
    template_name = 'profile_detail.html'
    context_object_name = 'profile'

    def get_object(self):
        return get_object_or_404(
            User, id=self.request.user.id
        )