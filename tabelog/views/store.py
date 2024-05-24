from django.views.generic import ListView
from tabelog.models import Store


class StoreListView(ListView):
    template_name = 'store_list.html'
    model = Store
    paginate_by = 10

    # 絞り込み機能
    def get_queryset(self, **kwargs):
        queryset = super().get_queryset(**kwargs)
        query = self.request.GET

        if q := query.get('q'): #python3.8以降
            queryset = queryset.filter(name__icontains=q)

        return queryset.order_by('-name')