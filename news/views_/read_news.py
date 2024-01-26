from django.views.generic import DetailView
from ..models import News as NewsModel


class ReadNews(DetailView):
    template_name = 'global/partials/read_post.html'
    context_object_name = 'post'
    model = NewsModel

    def get_queryset(self):
        # Filtro personalizado, pegar uma notícia com um slug | código em news/models
        qs = NewsModel.objects.get_one_news(self.kwargs['slug']).select_related('author')
        return qs

    def get_context_data(self, **kwargs):
        cd = super().get_context_data(**kwargs)

        cd['posts'] = NewsModel.objects.filter(is_published=True).order_by('-id')[0:3]

        return cd
