from django.urls import path
from allauth.account.views import LogoutView    #allauthの中にあるLogoutViewを持ってくる
from . import views

app_name = 'tabelog'

urlpatterns = [
    path('home/', views.HomeView.as_view(), name='home'),
    path('welcome/', views.WelcomeView.as_view(), name='welcome'),
    path('logout/', LogoutView.as_view(), name='logout')
]