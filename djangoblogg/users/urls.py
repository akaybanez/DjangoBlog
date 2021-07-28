from django.urls import path
from django.conf.urls import url

from . import views

app_name = 'users'

urlpatterns = [

    path('login',
         views.LoginView.as_view(),
         name='login'),

    path('logout',
         views.LogoutView,
         name='logout'),

    path('signup',
         views.SignupView.as_view(),
         name='signup')
]
