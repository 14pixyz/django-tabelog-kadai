from django.views.generic import TemplateView, ListView, DetailView, UpdateView, CreateView, DeleteView
from tabelog.models import Store, Category, Review, CustomUser
from django.urls import reverse_lazy
from ..forms import StoreForm, CategoryForm
from django.contrib.auth.views import LoginView
from django.contrib.auth.mixins import UserPassesTestMixin
from django.shortcuts import redirect


class BaseSupporterPermission(UserPassesTestMixin):
    def test_func(self):
        return self.request.user.is_authenticated and self.request.user.is_supporter

    def handle_no_permission(self):
        return redirect('tabelog:home')

    raise_exception = False
    login_url = reverse_lazy('tabelog:home')


class SupporterLoginView(LoginView):
    template_name = 'supporter/login.html'
    success_url = reverse_lazy('tabelog:admin-home')

    def get_success_url(self):
        if self.request.user.is_supporter:
            return reverse_lazy('tabelog:admin-home')
        else:
            return reverse_lazy('tabelog:home')


class HomeView(BaseSupporterPermission, TemplateView):
    template_name = 'admin_home.html'


class StoreListView(BaseSupporterPermission, ListView):
    template_name = 'admin_store_list.html'
    model = Store
    paginate_by = 10

    def get_queryset(self, **kwargs):
        queryset = super().get_queryset(**kwargs)
        query = self.request.GET

        # フィルタリング
        if store_name := query.get('store_name'):
            queryset = queryset.filter(name__icontains=store_name).order_by('id')
        # ソート
        if sort_by := query.get('sort_by'):
            queryset = queryset.order_by(sort_by)
        # カテゴリ
        if category := query.get('category'):
            queryset = queryset.filter(category__exact=category)

        return queryset

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['top_query'] = self.request.GET.get('top_query', '')
        context['store_name'] = self.request.GET.get('store_name', '')
        context['sort_by'] = self.request.GET.get('sort_by', '')
        context['select_category'] = self.request.GET.get('category')
        context['categorys'] = Category.objects.all()
        return context


# class StoreDetailView(BaseSupporterPermission, DetailView):
#     template_name = 'admin_store_detail.html'
#     model = Store

#     def get_context_data(self, **kwargs):
#         context = super().get_context_data(**kwargs)
#         context['reviews'] = Review.objects.filter(store__id=self.kwargs['pk'])
#         context['user'] = self.request.user
#         return context


class StoreNewView(BaseSupporterPermission, CreateView):
    template_name = 'admin_store_new_form.html'
    model = Store
    form_class = StoreForm

    def get_success_url(self) -> str:
        return reverse_lazy('tabelog:admin-store-list')


class StoreEditView(BaseSupporterPermission, UpdateView):
    template_name = 'admin_store_edit_form.html'
    model = Store
    form_class = StoreForm

    def get_success_url(self) -> str:
        return reverse_lazy('tabelog:admin-store-list')


class StoreDeleteView(BaseSupporterPermission, DeleteView):
    template_name = 'admin_store_confirm_delete.html'
    model = Store
    success_url = reverse_lazy('tabelog:admin-store-list')


class UserListView(BaseSupporterPermission, ListView):
    template_name = 'admin_user_list.html'
    model = CustomUser
    paginate_by = 10

    def get_queryset(self, **kwargs):
        queryset = super().get_queryset(**kwargs)
        query = self.request.GET

        # フィルタリング
        if user_email := query.get('user_email'):
            queryset = queryset.filter(email__icontains=user_email)
        return queryset

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['user_email'] = self.request.GET.get('user_email', '')
        return context


class CategoryListView(BaseSupporterPermission, ListView):
    template_name = 'admin_category_list.html'
    model = Category
    paginate_by = 10

    def get_queryset(self, **kwargs):
        queryset = super().get_queryset(**kwargs)
        query = self.request.GET

        # フィルタリング
        if category := query.get('category'):
            queryset = queryset.filter(name__icontains=category)
        return queryset

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['category'] = self.request.GET.get('category', '')
        return context


class CategoryEditView(BaseSupporterPermission, UpdateView):
    template_name = 'admin_category_edit_form.html'
    model = Category
    form_class = CategoryForm

    def get_success_url(self) -> str:
        return reverse_lazy('tabelog:admin-category-list')


class CategoryNewView(BaseSupporterPermission, CreateView):
    template_name = 'admin_category_new_form.html'
    model = Category
    form_class = CategoryForm

    def get_success_url(self) -> str:
        return reverse_lazy('tabelog:admin-category-list')


class CategoryDeleteView(BaseSupporterPermission, DeleteView):
    template_name = 'admin_category_confirm_delete.html'
    model = Category
    success_url = reverse_lazy('tabelog:admin-category-list')