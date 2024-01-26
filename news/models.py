from django.db import models
from tags.models import Tag
from django.contrib.auth.models import User
from django.utils.translation import gettext_lazy


# Create your models here.

# Função para filtrar meus objetos que estão publicados
class NewsManager(models.Manager):
    def get_published(self):
        return self.filter(is_published=True)

    def get_one_news(self, slug):
        return News.objects.filter(slug=slug, is_published=True)


class News(models.Model):
    # Permite criar um ‘manager’ para criar várias funções úteis
    # No caso, eu sempre recebo as notícias com 'is_published=True', criei uma função para fazer
    objects = NewsManager()

    author = models.ForeignKey(
        User, on_delete=models.CASCADE, blank=False, null=False, verbose_name=gettext_lazy('Author'))
    title = models.CharField(max_length=100, blank=False,
                             null=False, verbose_name=gettext_lazy('Title'))
    description = models.CharField(
        max_length=100, blank=False, null=False, verbose_name=gettext_lazy('Description'))
    content = models.TextField(
        blank=False, null=False, verbose_name=gettext_lazy('Content'))
    image = models.ImageField(
        upload_to='news/%Y/%m/%d', blank=True, null=True, verbose_name=gettext_lazy('Image'))
    slug = models.SlugField(unique=True, blank=True, max_length=200)
    type = models.CharField(choices=(
        ('News', 'Notícias'),
        ('MainNews', 'Notícia principail'),
        ('SecondaryNewsTop', 'Notícias secundárias'),
        ('ThirdlyNews', 'Notícias terciária ')
    ), max_length=30, default='News', verbose_name=gettext_lazy('Type'))
    is_published = models.BooleanField(
        default=False, blank=False, null=False, verbose_name=gettext_lazy('Is Published'))
    created_at = models.DateTimeField(auto_now_add=True, blank=True, null=True)
    updated_at = models.DateTimeField(auto_now=True, blank=True, null=True)
    tags = models.ManyToManyField(Tag, blank=True, null=True)

    def __str__(self) -> models.CharField:
        return self.title

    class Meta:
        verbose_name_plural = gettext_lazy('News')
        verbose_name = gettext_lazy('News')
