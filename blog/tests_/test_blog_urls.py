from django.test import TestCase
from django.urls import reverse


class BlogNewsUrl(TestCase):
    def test_url_create_post_is_correct(self):
        # Http response | status code e várias outras coisas...
        url = reverse('blog:create_post')

        self.assertEqual('/blog/create/post/', url)

    def test_url_all_users_is_correct(self):
        # Http response | status code e várias outras coisas...
        url = reverse('blog:all_users')

        self.assertEqual('/blog/all/users/', url)

    def test_url_all_posts_is_correct(self):
        # Http response | status code e várias outras coisas...
        url = reverse('blog:all_posts')

        self.assertEqual('/blog/all/posts/', url)
