from django.views.generic import ListView, DetailView
from tags.models import Tag
from ..models import News


class Tags(ListView):
    template_name = 'news/all_tags.html'
    model = Tag
    context_object_name = 'news'

    def get_queryset(self):
        qs = super().get_queryset()
        qs = qs.filter(slug=self.kwargs.get('slug')).first()

        return qs


    def get_context_data(self, *, object_list=None, **kwargs):
        cd = super().get_context_data(object_list=None, **kwargs)
        cd['page_obj'] = News.objects.filter(tags__slug=self.kwargs.get('slug'))
        cd['title'] = self.kwargs.get('slug')

        return cd
