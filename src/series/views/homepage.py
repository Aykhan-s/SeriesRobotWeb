from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator
from account.models import User


@login_required(login_url='/account/login')
def homepage_view(request):
    series = User.objects.get(id=request.user.id).series.all().order_by('-id')
    page = request.GET.get('page')
    paginator = Paginator(series, 5)

    return render(request, 'homepage.html', context={'series': paginator.get_page(page)})