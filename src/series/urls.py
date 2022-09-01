from django.urls import path
from series import views


urlpatterns = [
    path('', views.homepage_view, name='homepage'),
    path('series/add/', views.AddSeriesView.as_view(), name='add-series'),
    path('series/update/<slug:slug>', views.UpdateSeriesView.as_view(), name='update-series'),
    path('series/delete/<slug:slug>', views.SeriesDeleteView.as_view(), name='delete-series'),
    path('series/new-episodes/', views.new_episodes_view, name='new-episodes'),
]