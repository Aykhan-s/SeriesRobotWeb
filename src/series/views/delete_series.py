from series.models import SeriesModel
from django.views.generic import DeleteView
from django.urls import reverse_lazy, reverse
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib import messages


class SeriesDeleteView(LoginRequiredMixin, DeleteView):
    login_url = reverse_lazy('login')
    template_name = 'article_deletion_confirmation.html'

    def get_success_url(self):
        messages.success(self.request, 'Series Deleted')
        return reverse('homepage')

    def get_queryset(self):
        return SeriesModel.objects.filter(slug=self.kwargs['slug'], user=self.request.user)