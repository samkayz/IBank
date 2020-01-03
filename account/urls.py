from django.urls import path
from . import views

urlpatterns = [
    path('signup', views.signup, name='signup'),
    path('', views.index, name='index'),
    path('index', views.index, name='index'),
    path('home', views.home, name='home'),
    path('logout', views.logout, name='logout'),
    path('profile', views.profile, name='profile'),
    path('create_acct', views.create_acct, name='create_acct'),
    path('acct_list', views.acct_list, name='acct_list'),
    path('verify', views.verify, name='verify'),
    path('fund_transfer', views.fund_transfer, name='fund_transfer'),
    path('history', views.history, name='history'),
    path('book_loan', views.book_loan, name='book_loan'),
    path('statement', views.statement, name='statement'),
]
