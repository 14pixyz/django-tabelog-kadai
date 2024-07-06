from django.views.generic import UpdateView, TemplateView, DetailView
from tabelog.models import CustomUser
from django.contrib.auth.mixins import UserPassesTestMixin
from django.urls import reverse_lazy
from django.shortcuts import redirect



class MemberView(UserPassesTestMixin, DetailView):
    # ユーザーの種類を判定している
    def test_func(self):
        return self.request.user.is_authenticated and int(self.request.user.id) == self.kwargs['pk']

    def handle_no_permission(self):
        return redirect('tabelog:store-list')

    raise_exception = False
    login_url = reverse_lazy('tabelog:store-list')

    template_name = 'member_menu.html'
    model = CustomUser


class MemberEditView(UserPassesTestMixin, UpdateView):
    # ユーザーの種類を判定している
    def test_func(self):
        return self.request.user.is_authenticated

    def handle_no_permission(self):
        return redirect('tabelog:store-list')

    raise_exception = False
    login_url = reverse_lazy('tabelog:store-list')

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
        return redirect('tabelog:store-list')

    raise_exception = False
    login_url = reverse_lazy('tabelog:store-list')

    template_name = 'email_edit_form.html'
    model = CustomUser
    fields = ("email",)

    def get_success_url(self):
        return reverse_lazy('tabelog:member-menu', kwargs={'pk': self.object.id})