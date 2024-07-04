import requests
import stripe

from myproject import settings

from django.contrib.auth.mixins import UserPassesTestMixin
from django.shortcuts import render, redirect
from django.urls import reverse_lazy
from django.views.generic import View

from tabelog.models import CustomUser, UserType


stripe.api_key = settings.STRIPE_SECRET_KEY

class CreditRegisterView(UserPassesTestMixin, View):
    def test_func(self):
        return self.request.user.is_authenticated and self.request.user.is_free

    def handle_no_permission(self):
        return redirect('tabelog:store-list')

    raise_exception = False
    login_url = reverse_lazy('tabelog:store-list')

    def get(self, request):
        ctx = {
            'stripe_public_key': settings.STRIPE_PUBLIC_KEY,
        }
        return render(request, 'credit_entry.html', ctx)

    def post(self, request):
        email = self.request.user.email
        customer = stripe.Customer.create(
            name=email,
            email=email,
        )

        card = stripe.Customer.create_source(
            customer.id,
            source=request.POST.get('stripeToken'), #.get()に変更
        )

        subscription = stripe.Subscription.create(
            customer=customer.id,
            items=[{'price': settings.STRIPE_PRICE_ID}],
        )

        custom_user = CustomUser.objects.get(email=email)
        custom_user.stripe_customer_id = customer.id
        custom_user.stripe_card_id = card.id
        custom_user.stripe_card_last4_no = card.last4
        custom_user.stripe_subscription_id = subscription.id
        custom_user.user_type = UserType.PAID
        custom_user.save()

        return redirect('tabelog:store-list')


class SubscriptionCancelView(UserPassesTestMixin, View):
    def test_func(self):
        return self.request.user.is_authenticated and self.request.user.is_paid

    raise_exception = False
    login_url = reverse_lazy('tabelog:store-list')

    def get(self, request):
        return render(request, 'paid_membership_cancel.html')

    def post(self, request):
        custom_user = CustomUser.objects.get(email=request.user.email)
        stripe.Subscription.delete(custom_user.stripe_subscription_id)
        stripe.Customer.delete(custom_user.stripe_customer_id)

        custom_user.stripe_customer_id = None
        custom_user.stripe_card_id = None
        custom_user.stripe_subscription_id = None
        custom_user.user_type = UserType.FREE
        custom_user.save()

        return redirect('tabelog:store-list')


class CreditUpdateView(UserPassesTestMixin, View):
    def test_func(self):
        return self.request.user.is_authenticated and self.request.user.is_paid

    raise_exception = False
    login_url = reverse_lazy('tabelog:store-list')

    def get(self, request):
        email = self.request.user.email
        custom_user = CustomUser.objects.get(email=email)
        url = f'https://api.stripe.com/v1/customers/{custom_user.stripe_customer_id}/cards/{custom_user.stripe_card_id}'
        response = requests.get(url, auth=(settings.STRIPE_SECRET_KEY, ''))

        stripe_customer_json = response.json()

        ctx = {
            'card_brand': stripe_customer_json['brand'],
            'card_last4': stripe_customer_json['last4'],
            'stripe_public_key': settings.STRIPE_PUBLIC_KEY,
        }
        return render(request, 'credit_update.html', ctx)

    def post(self, request):
        email = self.request.user.email
        custom_user = CustomUser.objects.get(email=email)

        card = stripe.Customer.create_source(
            custom_user.stripe_customer_id,
            source=request.POST.get('stripeToken'), #.get()に変更
        )

        stripe.Customer.delete_source(
            custom_user.stripe_customer_id,
            custom_user.stripe_card_id,
        )

        custom_user.stripe_card_id = card.id
        custom_user.save()

        return redirect('tabelog:store-list')


