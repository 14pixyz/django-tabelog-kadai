from django.urls import path
from .views import home, credit

app_name = 'tabelog'

urlpatterns = [
    path('home/', home.HomeView.as_view(), name='home'),
    path('welcome/', home.WelcomeView.as_view(), name='welcome'),
    path('member/', home.MemberView.as_view(), name='member-menu'),

    path('credit/register/', credit.CreditRegisterView.as_view(), name='credit-register'),
    path('credit/update/', credit.CreditUpdateView.as_view(), name='credit-update'),
    path('subscription/cancel/', credit.SubscriptionCancelView.as_view(), name='subscription-cancel'),
]