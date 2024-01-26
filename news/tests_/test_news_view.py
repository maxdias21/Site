from .test_news_base import NewsBaseTest
from django.urls import resolve, reverse
from news import views_


class NewsViewTest(NewsBaseTest):
    def setUp(self):
        self.url = resolve(reverse('news:index'))

    def test_view_is_correct(self):
        # Coleta algumas informações com base na url que passar | func, args, kwargs, url_name...
        view = self.url

        self.assertIs(views_.NewsIndex, view.func.view_class)

    def test_app_name_is_correct(self):
        # coleta algumas informações com base na url que passar | func, args, kwargs, url_name...
        view = self.url

        self.assertIs(view.app_name, 'news')

    def test_recipe_view_status_code_is_200(self):
        # coleta algumas informações com base na url que passar | func, args, kwargs, url_name...
        view = self.url

        # Pegar o HTML da página | converter para utf-8
        content = self.client.get(reverse('news:index'))

        self.assertIs(content.status_code, 200)

    def test_recipe_template_is_correct(self):
        # Pegar o HTML da página | converter para utf-8
        content = self.client.get(reverse('news:index'))

        self.assertTemplateUsed(content, 'news/index.html')
