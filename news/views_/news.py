from typing import Any
from django.db.models.query import QuerySet
from django.views.generic import ListView
from ..models import News as NewsModel
from blog.models import Blog
from authors.models import AuthorRegister
from tags.models import Tag


class NewsIndex(ListView):
    template_name = 'news/index.html'
    model = NewsModel
    context_object_name = 'news'

    # Usei para fazer filtros personalizados
    def get_queryset(self) -> QuerySet[Any]:
        qs = super().get_queryset()

        # Filtrar para obter apenas notícias que estão publicadas
        qs = qs.filter(is_published=True).order_by('-id')

        return qs

    # Usei para adicionar o campo de usuários no meu contexto
    def get_context_data(self, **kwargs: Any) -> dict[str, Any]:
        cd = super().get_context_data()

        # Pegar notícia principal
        cd['main_news'] = self.get_queryset().filter(type='MainNews', is_published=True).order_by('-id').first()

        # Pegar notícia secundária
        cd['secondary_news'] = self.get_queryset().filter(type='SecondaryNewsTop', is_published=True).order_by(
            '-id').first()

        # Pegar notícia terciária
        cd['thirdly_news'] = self.get_queryset().filter(type='ThirdlyNews', is_published=True).order_by('-id').first()

        # Criar chave de "usuários" e pegar apenas os últimos 5
        cd['authors'] = AuthorRegister.objects.filter().select_related('author').order_by('-id')[0:5]

        # Pegar últimos 5 posts
        cd['posts'] = Blog.objects.get_five_posts_that_is_published().select_related('author')

        # Pegar tags
        cd['tags'] = Tag.objects.all()[0:20]

        return cd
