from django.test import TestCase
from utils.testMixin.tests import TestMixin
from ..models import Blog


class BlogBase(TestCase, TestMixin):
    def setUp(self):
        super().setUp()
        self.form_data_create_post = {
            'title': 'Title',
            'description': 'Description',
            'content': 'Content',
            'image': ''
        }

    def create_post(self, author='', title='Title', description='Description', content='This is my content', image='',
                    slug='teste', is_published=True):
        if not author:
            # Criar autor
            author = self.create_user()

        return Blog.objects.create(author=author, title=title, description=description, content=content, image=image,
                                   slug=slug, is_published=is_published)



