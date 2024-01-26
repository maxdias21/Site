from django.db import models
from django.contrib.auth.models import User
from django.utils.translation import gettext_lazy


# Create your models here.

class BlogManager(models.Manager):
    def get_five_posts_that_is_published(self):
        return Blog.objects.filter().order_by('-id')[:5]

    def get_one_post(self, slug):
        return Blog.objects.filter(is_published=True, slug=slug).first()

    def get_post_is_published(self):
        return Blog.objects.filter(is_published=True)


class Blog(models.Model):
    objects = BlogManager()
    author = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True,
                               verbose_name=gettext_lazy('Author'))
    title = models.CharField(max_length=100, blank=False, null=False, verbose_name=gettext_lazy('Title'))
    description = models.TextField(max_length=250, blank=False, null=False, verbose_name=gettext_lazy('Description'))
    content = models.CharField(verbose_name=gettext_lazy('Content'), max_length=2000)
    created_at = models.DateTimeField(auto_now_add=True, blank=True, null=True)
    updated_at = models.DateTimeField(auto_now=True, blank=True, null=True)
    image = models.ImageField(upload_to='blog/covers/%Y/%m/%d', null=True, blank=True,
                              verbose_name=gettext_lazy('Image'))
    is_published = models.BooleanField(default=False, verbose_name=gettext_lazy('Is published'))
    slug = models.SlugField(unique=True, blank=True, max_length=255)
    qty_read = models.IntegerField(default=0, verbose_name=gettext_lazy('Qty read'))


    def __str__(self):
        return self.title

    class Meta:
        verbose_name_plural = gettext_lazy('Blog')
        verbose_name = gettext_lazy('Blog')
