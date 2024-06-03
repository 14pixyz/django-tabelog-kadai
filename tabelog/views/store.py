from django.views.generic import ListView, DetailView, View
from tabelog.models import Store, Category, Review, Reservation
from django.views.generic.edit import CreateView, UpdateView

from django.urls import reverse_lazy
from django.contrib.auth.mixins import UserPassesTestMixin
from django.shortcuts import redirect, render

class StoreListView(ListView):
    template_name = 'store_list.html'
    model = Store
    paginate_by = 10

    def get_queryset(self, **kwargs):
        queryset = super().get_queryset(**kwargs)
        query = self.request.GET

        # トップ画面からの検索
        if top_query := query.get('top_query'):
            queryset = queryset.filter(name__icontains=top_query).order_by('id')
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


class StoreDetailView(DetailView):
    template_name = 'store_detail.html'
    model = Store

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['reviews'] = Review.objects.filter(store__id=self.kwargs['pk'])
        return context


class ReviewCreateView(UserPassesTestMixin, CreateView):
    # ユーザーの種類を判定している
    def test_func(self):
        return self.request.user.is_authenticated and self.request.user.is_paid

    def handle_no_permission(self):
        return redirect('tabelog:home')

    raise_exception = False
    login_url = reverse_lazy('tabelog:home')

    template_name = 'review_new_form.html'
    model = Review
    fields = ("content", "star")

    # フォーム保存時の動作
    def form_valid(self, form):
        object = form.save(commit=False)
        object.user = self.request.user
        object.store_id = self.kwargs['store_id']
        object.save()
        return super().form_valid(form)

    def get_success_url(self) -> str:
        return reverse_lazy('tabelog:store-detail', kwargs={'pk': self.kwargs['store_id']})


class ReviewEditView(UserPassesTestMixin, UpdateView):
    def test_func(self):
        # レビューIDを取得して、紐づいているユーザーIDと現在アクセスしているユーザーのIDが一致するかを確認している。
        review = Review.objects.get(id=self.kwargs['pk'])
        return self.request.user.is_authenticated and self.request.user.is_paid and review.user.id == self.request.user.id

    def handle_no_permission(self):
        return redirect('tabelog:home')

    raise_exception = False
    login_url = reverse_lazy('tabelog:home')

    template_name = 'review_edit_form.html'
    model = Review
    fields = ("content", "star")

    def get_success_url(self) -> str:
        return reverse_lazy('tabelog:store-detail', kwargs={'pk': self.object.store.id})


class ReservationCreateView(UserPassesTestMixin, CreateView):
    # ユーザーの種類を判定している
    def test_func(self):
        return self.request.user.is_authenticated and self.request.user.is_paid

    def handle_no_permission(self):
        return redirect('tabelog:home')

    raise_exception = False
    login_url = reverse_lazy('tabelog:home')

    template_name = 'reservation_new_form.html'
    model = Reservation
    fields = ("date", "time", "people")

    # フォーム保存時の動作
    def form_valid(self, form):
        object = form.save(commit=False)
        object.user = self.request.user
        object.store_id = self.kwargs['store_id']
        object.save()
        return super().form_valid(form)

    def get_success_url(self) -> str:
        return reverse_lazy('tabelog:store-detail', kwargs={'pk': self.kwargs['store_id']})


class ReservationListView(UserPassesTestMixin, ListView):
    def test_func(self):
        return self.request.user.is_authenticated and self.request.user.is_paid

    def handle_no_permission(self):
        return redirect('tabelog:home')

    raise_exception = False
    login_url = reverse_lazy('tabelog:home')

    template_name = 'reservation_list.html'
    model = Reservation
    paginate_by = 10

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['reservations'] = Reservation.objects.all()
        return context


class ReservationCancelView(UserPassesTestMixin, View):
    def test_func(self):
        return self.request.user.is_authenticated and self.request.user.is_paid

    def handle_no_permission(self):
        return redirect('tabelog:home')

    def get(self, request):
        return render(request, 'reservation_cancel.html')

    def post(self):
        reservation = Reservation.objects.get(id=self.kwargs['pk']) #？　2024-06-03 07:29:59

        reservation.date = None
        reservation.time = None
        reservation.people = None
        reservation.save()

        return redirect('tabelog:reservation-list')

    raise_exception = False
    login_url = reverse_lazy('tabelog:home')