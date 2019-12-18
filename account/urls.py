from django.urls import path
from . import views

urlpatterns = [
    path('signup', views.signup, name='signup'),
    path('index', views.index, name='index'),
    path('home', views.home, name='home'),
    path('logout', views.logout, name='logout'),
    path('profile', views.profile, name='profile'),
    path('create_acct', views.create_acct, name='create_acct'),
]
