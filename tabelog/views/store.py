from django.views import generic

class StoreListView(generic.TemplateView):
    template_name = 'store_list.html'