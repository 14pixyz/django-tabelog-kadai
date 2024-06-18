from django.views.generic import UpdateView, TemplateView, DetailView
from tabelog.models import CustomUser
from django.contrib.auth.mixins import UserPassesTestMixin
from django.urls import reverse_lazy
from django.shortcuts import redirect


class HomeView(TemplateView):
    template_name = 'home.html'


class MemberView(UserPassesTestMixin,DetailView):
    # ユーザーの種類を判定している
    def test_func(self):
        return self.request.user.is_authenticated

    def handle_no_permission(self):
        return redirect('tabelog:home')

    raise_exception = False
    login_url = reverse_lazy('tabelog:home')

    template_name = 'member_menu.html'
    model = CustomUser


class MemberEditView(UserPassesTestMixin, UpdateView):
    # ユーザーの種類を判定している
    def test_func(self):
        return self.request.user.is_authenticated

    def handle_no_permission(self):
        return redirect('tabelog:home')

    raise_exception = False
    login_url = reverse_lazy('tabelog:home')

    template_name = 'member_edit_form.html'
    model = CustomUser
    fields = ("username",)

    def get_success_url(self) -> str:
        return reverse_lazy('tabelog:member-menu', kwargs={'pk': self.object.id})


class EmailEditView(UserPassesTestMixin, UpdateView):
    # ユーザーの種類を判定している
    def test_func(self):
        return self.request.user.is_authenticated

    def handle_no_permission(self):
        return redirect('tabelog:home')

    raise_exception = False
    login_url = reverse_lazy('tabelog:home')

    template_name = 'email_edit_form.html'
    model = CustomUser
    fields = ("email",)

    def get_success_url(self):
        return reverse_lazy('tabelog:member-menu', kwargs={'pk': self.object.id})