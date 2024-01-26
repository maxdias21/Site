from django.test import TestCase
from utils.testMixin.tests import TestMixin
from news.models import News


# Classe útil para criar notícias sem ficar a repetir código na hora do teste
class NewsMixin(TestMixin):
    def create_news(self, author=None, title='News Title', description='Description', content='Content', image='image',
                    slug='NewsSlug', type='News', is_published=False):

        if author == None:
            author = self.create_user()

        return News.objects.create(author=author, title=title, description=description, content=content, image=image,
                                   slug=slug, type=type, is_published=is_published)

    def create_many_news(self, qnt=10):
        for x in range(0, qnt + 1):
            author = self.create_user(first_name=f'First {x}', last_name=f'Last {x}', email=f"email{x}@gmail.com",
                                      username=f'username{x}')
            self.create_news(author=author, slug=f'slug{x}', is_published=True)


class NewsBaseTest(TestCase, NewsMixin):
    def setUp(self):
        return super().setUp()
