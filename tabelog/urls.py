from django.urls import path
from .views import home, credit, store

from django.conf import settings
from django.conf.urls.static import static


app_name = 'tabelog'

urlpatterns = [
    path('home/', home.HomeView.as_view(), name='home'),
    path('welcome/', home.WelcomeView.as_view(), name='welcome'),
    path('member/', home.MemberView.as_view(), name='member-menu'),

    path('credit/register/', credit.CreditRegisterView.as_view(), name='credit-register'),
    path('credit/update/', credit.CreditUpdateView.as_view(), name='credit-update'),
    path('subscription/cancel/', credit.SubscriptionCancelView.as_view(), name='subscription-cancel'),

    path('store/list/', store.StoreListView.as_view(), name='store-list')
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)