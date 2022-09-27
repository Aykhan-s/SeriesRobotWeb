from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator
from account.models import User


@login_required(login_url='/account/login')
def homepage_view(request):
    user = User.objects.get(id=request.user.id)
    series_true = user.series.filter(show=True).order_by('-id')
    series_false = user.series.filter(show=False).order_by('-id')
    page = request.GET.get('page')
    paginator = Paginator(list(series_true) + list(series_false), 5)

    return render(request, 'homepage.html', context={'series': paginator.get_page(page)})