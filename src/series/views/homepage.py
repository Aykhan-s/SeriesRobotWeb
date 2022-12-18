from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator
from account.models import User
from django.db.models import Q


@login_required(login_url='/account/login')
def homepage_view(request):
    user = User.objects.get(id=request.user.id)

    if request.GET.get('new') == 'true':
        series = user.series.filter(~Q(new_episodes_count=0)).order_by('-id')

    else: series = user.series.filter().order_by('-id')

    if search := request.GET.get('search'):
        series = series.filter(
            Q(title__icontains=search)
        )

    page = request.GET.get('page')
    paginator = Paginator(series, 5)

    return render(request, 'homepage.html', context={'series': paginator.get_page(page)})