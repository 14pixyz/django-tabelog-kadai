from django.urls import path
from . import views

app_name = 'tabelog'

urlpatterns = [
    path('home/', views.HomeView.as_view(), name='home'),
    path('welcome/', views.WelcomeView.as_view(), name='welcome'),
]