from django.views.generic import ListView, DetailView
from tabelog.models import Store


class StoreListView(ListView):
    template_name = 'store_list.html'
    model = Store
    paginate_by = 10

    def get_queryset(self, **kwargs):
        queryset = super().get_queryset(**kwargs)
        query = self.request.GET

        # フィルタリング
        if q := query.get('q'):
            queryset = queryset.filter(name__icontains=q).order_by('budget')
        # ソート
        if sort_by := query.get('sort_by'):
            queryset = queryset.order_by(sort_by)

        return queryset

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['sort_by'] = self.request.GET.get('sort_by', '')
        context['q'] = self.request.GET.get('q', '')
        return context


class StoreDetailView(DetailView):
    template_name = 'store_detail.html'
    model = Store