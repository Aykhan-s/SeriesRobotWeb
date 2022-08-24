from django.urls import path
from account import views
from django.contrib.auth import views as auth_views


urlpatterns = [
    path('login', auth_views.LoginView.as_view(
        template_name = 'login.html'
        ), name='login'),
    path('register', views.register_view, name='register'),
    path('logout', views.logout_view, name='logout'),
    path('change-password', views.change_password_view, name='change-password'),
    path('profile-editing', views.profile_editing_view, name='profile-editing'),
    path('profile', views.ProfileDetailView.as_view(), name='profile')
]
