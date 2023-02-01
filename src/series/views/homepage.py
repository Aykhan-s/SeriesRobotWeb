from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator
from account.models import User
from django.db.models import Q


@login_required(login_url='/account/login')
def homepage_view(request):
    user = User.objects.get(id=request.user.id)

    type_ = request.GET.get('type')
    if type_ == 'unwatched':
        series = user.series.filter(~Q(new_episodes_count=0)).order_by('-id')

    elif type_ == 'watched':
        series = user.series.filter(new_episodes_count=0).order_by('-id')

    else:
        type_ = 'all'
        series = user.series.filter().order_by('-id')

    search = request.GET.get('search', 'None')
    if search != 'None':
        series = series.filter(
            Q(title__icontains=search)
        )

    def kwargs():
        queries = request.GET.copy()
        queries.pop('page', 0)
        return queries.urlencode()

    page = request.GET.get('page')
    paginator = Paginator(series, 5)

    return render(request, 'homepage.html', context={'series': paginator.get_page(page),
                                                    'kwargs': kwargs(),
                                                    'type': type_})