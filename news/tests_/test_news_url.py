from django.test import TestCase
from django.urls import reverse

class NewsUrlTest(TestCase):
    def test_news_url_is_correct(self):
        # Http response | status code e várias outras coisas...
        url = reverse('news:index')

        self.assertIn(url,'/')