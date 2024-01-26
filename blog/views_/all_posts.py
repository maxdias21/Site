from django.views.generic import ListView
from ..models import Blog


class AllPosts(ListView):
    template_name = 'blog/all_posts.html'
    model = Blog
    context_object_name = 'posts'
    paginate_by = 19

    def get_queryset(self):
        qs = super().get_queryset()
        qs = qs.filter(is_published=True)

        return qs

    def get_context_data(self, **kwargs):
        cd = super().get_context_data(**kwargs)

        return cd
