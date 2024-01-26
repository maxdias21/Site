from django.views.generic import ListView
from authors.models import AuthorRegister
from ..models import Blog
from django.db.models import Q
from news.models import News


class Search(ListView):
    template_name = 'blog/search.html'
    model = Blog
    context_object_name = 'posts'

    def setup(self, request, *args, **kwargs):
        super().setup(request, *args, **kwargs)

        # Pegar o "name" do meu campo search
        # Está na navegação do boostrap
        self.search_term = request.GET.get('q', '')

    def get_queryset(self):
        qs = super().get_queryset()

        # __icontains = Como se fosse o Like
        # Q = Troca para "ou" ao invés de "e"
        qs = qs.filter(Q(title__icontains=self.search_term) | Q(description__icontains=self.search_term),
                       is_published=True)

        return qs

    def get_context_data(self, *, object_list=None, **kwargs):
        cd = super().get_context_data(object_list=None, **kwargs)
        # Pegar quantidade de posts com o termo da busca
        cd['qnt_posts_blog'] = len(self.get_queryset())

        # Pegar usuários
        cd['users'] = AuthorRegister.objects.filter(
            Q(author__first_name__icontains=self.search_term) | Q(author__last_name__icontains=self.search_term) | Q(
                author__email__icontains=self.search_term))
        cd['qnt_users'] = len(cd['users'])

        # Pegar notícias
        cd['news'] = News.objects.filter(
            Q(title__icontains=self.search_term) | Q(description__icontains=self.search_term))
        cd['qnt_news'] = len(cd['news'])

        # Pegar notícias com tags
        cd['news_tags'] = News.objects.filter(tags__name__icontains=self.search_term)
        cd['qtn_tags'] = len(cd['news_tags'])

        cd['search_term'] = self.search_term

        return cd
