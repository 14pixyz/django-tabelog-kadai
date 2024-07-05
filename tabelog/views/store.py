from django.views.generic import ListView, DetailView
from tabelog.models import Store, Category, Review, Reservation, Favarit
from django.views.generic.edit import CreateView, UpdateView, DeleteView

from django.urls import reverse_lazy
from django.contrib.auth.mixins import UserPassesTestMixin
from django.shortcuts import redirect, get_object_or_404

from ..forms import ReservationForm, ReviewForm


class BasePaidPermission(UserPassesTestMixin):
    # ユーザーの種類を判定している
    def test_func(self):
        return self.request.user.is_authenticated and self.request.user.is_paid

    def handle_no_permission(self):
        return redirect('tabelog:store-list')

    raise_exception = False
    login_url = reverse_lazy('tabelog:store-list')


class StoreListView(ListView):
    template_name = 'store_list.html'
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


class StoreDetailView(DetailView):
    template_name = 'store_detail.html'
    model = Store

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['reviews'] = Review.objects.filter(store__id=self.kwargs['pk'])
        context['is_favarit'] = Favarit.objects.filter(store__id=self.kwargs['pk'], user__id=self.request.user.id).exists
        context['user'] = self.request.user
        return context


class ReviewCreateView(UserPassesTestMixin, CreateView):
    # ユーザーの種類を判定している
    def test_func(self):
        return self.request.user.is_authenticated and self.request.user.is_paid

    def handle_no_permission(self):
        return redirect('tabelog:store-list')

    raise_exception = False
    login_url = reverse_lazy('tabelog:store-list')

    template_name = 'review_new_form.html'
    form_class = ReviewForm

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
        return redirect('tabelog:store-list')

    raise_exception = False
    login_url = reverse_lazy('tabelog:store-list')

    template_name = 'review_edit_form.html'
    form_class = ReviewForm

    def get_queryset(self):
        return Review.objects.filter(user=self.request.user)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        return context

    def get_success_url(self) -> str:
        return reverse_lazy('tabelog:store-detail', kwargs={'pk': self.object.store.id})


class ReservationCreateView(BasePaidPermission, CreateView):
    template_name = 'reservation_new_form.html'
    model = Reservation
    form_class = ReservationForm

    # フォーム保存時の動作
    def form_valid(self, form):
        object = form.save(commit=False)
        object.user = self.request.user
        object.store_id = self.kwargs['store_id']
        object.save()
        return super().form_valid(form)

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        store_id = self.kwargs.get('store_id')  # URLパラメータからstore_idを取得
        store = get_object_or_404(Store, id=store_id)  # Storeオブジェクトを取得
        kwargs['store'] = store  # フォームにstoreオブジェクトを渡す
        return kwargs

    def get_success_url(self) -> str:
        return reverse_lazy('tabelog:store-detail', kwargs={'pk': self.kwargs['store_id']})


class ReservationListView(UserPassesTestMixin, ListView):
    def test_func(self):
        return self.request.user.is_authenticated and self.request.user.is_paid

    def handle_no_permission(self):
        return redirect('tabelog:store-list')

    raise_exception = False
    login_url = reverse_lazy('tabelog:store-list')

    template_name = 'reservation_list.html'
    model = Reservation
    paginate_by = 10

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['reservations'] = Reservation.objects.all()
        return context


class ReservationDeleteView(UserPassesTestMixin, DeleteView):
    def test_func(self):
        return self.request.user.is_authenticated and self.request.user.is_paid

    def handle_no_permission(self):
        return redirect('tabelog:store-list')

    template_name = 'reservation_confirm_delete.html'
    model = Reservation
    success_url = reverse_lazy('tabelog:reservation-list')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['reservation'] = self.get_object()
        return context


# お気に入り
class FavaritCreateView(UserPassesTestMixin, CreateView):
    def test_func(self):
        return self.request.user.is_authenticated and self.request.user.is_paid

    def handle_no_permission(self):
        return redirect('tabelog:store-list')

    # フォーム保存時の動作
    def post(self, request, *args, **kwargs):
        Favarit.objects.create(user_id=request.user.id, store_id=kwargs['store_id'])
        return redirect('tabelog:store-detail', kwargs['store_id'])


class FavaritDeleteView(UserPassesTestMixin, CreateView):
    def test_func(self):
        return self.request.user.is_authenticated and self.request.user.is_paid

    def handle_no_permission(self):
        return redirect('tabelog:store-list')

    def post(self, request,**kwargs):
        Favarit.objects.filter(user_id=request.user.id, store_id=kwargs['store_id']).delete()
        return redirect('tabelog:store-detail', kwargs['store_id'])


class FavaritListView(UserPassesTestMixin, ListView):
    def test_func(self):
        return self.request.user.is_authenticated and self.request.user.is_paid

    def handle_no_permission(self):
        return redirect('tabelog:store-list')

    raise_exception = False
    login_url = reverse_lazy('tabelog:store-list')

    template_name = 'favarit_list.html'
    model = Favarit
    paginate_by = 10

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['favarits'] = Favarit.objects.all()
        return context