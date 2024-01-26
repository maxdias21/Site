from django.views.generic import ListView
from ..models import News as NewsModel


class AllNews(ListView):
    paginate_by = 10
    template_name = 'news/all_news.html'
    model = NewsModel
    context_object_name = 'post'

    def get_queryset(self):
        qs = NewsModel.objects.get_published()

        return qs

    def get_context_data(self, *, object_list=None, **kwargs):
        cd = super().get_context_data(**kwargs)

        return cd
