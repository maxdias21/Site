from django.views.generic import DetailView
from ..models import Blog
from news.models import News as NewsModel


class ReadBlogNews(DetailView):
    template_name = 'global/partials/read_post.html'
    model = Blog
    context_object_name = 'post'

    def get_context_data(self, **kwargs):
        cd = super().get_context_data(**kwargs)

        cd['posts'] = NewsModel.objects.filter(is_published=True).order_by('-id')[0:3]

        return cd