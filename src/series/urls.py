from django.urls import path
from series import views


urlpatterns = [
    path('', views.homepage_view, name='homepage'),
    path('series/add', views.AddSeriesView.as_view(), name='add-series'),
]