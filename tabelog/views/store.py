from django.views.generic import ListView, DetailView
from tabelog.models import Store, Category, Review

from django.views.generic.edit import CreateView

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
        context['reviews'] = Review.objects.all()
        return context


class ReviewCreateView(CreateView):
    template_name = 'review_form.html'
    model = Review
    fields = ("content", "star", "store")

    def form_valid(self, form):
        # ユーザーを投稿者として保存できるようにする
        object = form.save(commit=False)
        object.user = self.request.user
        object.save()
        return super().form_valid(form)
