from django.urls import path
from .views import home, credit, store

from django.conf import settings
from django.conf.urls.static import static


app_name = 'tabelog'

urlpatterns = [
    path('home/', home.HomeView.as_view(), name='home'),
    path('member/<int:pk>/', home.MemberView.as_view(), name='member-menu'),
    path('member/edit/<int:pk>/', home.MemberEditView.as_view(), name='member-edit-form'),
    path('member/edit/email/<int:pk>/', home.EmailEditView.as_view(), name='email-edit-form'),


    path('credit/register/', credit.CreditRegisterView.as_view(), name='credit-register'),
    path('credit/update/', credit.CreditUpdateView.as_view(), name='credit-update'),
    path('subscription/cancel/', credit.SubscriptionCancelView.as_view(), name='subscription-cancel'),

    path('store/list/', store.StoreListView.as_view(), name='store-list'),
    path('store/detail/<int:pk>/', store.StoreDetailView.as_view(), name='store-detail'),

    path('review/new/store/<int:store_id>/',store.ReviewCreateView.as_view(), name='review-new-form'),
    path('review/edit/<int:pk>/',store.ReviewEditView.as_view(), name='review-edit-form'),

    path('reservation/new/store/<int:store_id>/',store.ReservationCreateView.as_view(), name='reservation-new-form'),
    path('reservation/list/',store.ReservationListView.as_view(), name='reservation-list'),
    path('reservation/cancel/<int:pk>/',store.ReservationDeleteView.as_view(), name='reservation-cancel'),

    path('favarit/create/store/<int:store_id>/', store.FavaritCreateView.as_view(), name='favarit-create'),
    path('favarit/delete/store/<int:store_id>/', store.FavaritDeleteView.as_view(), name='favarit-delete'),
    path('favarit/list/', store.FavaritListView.as_view(), name='favarit-list'),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)