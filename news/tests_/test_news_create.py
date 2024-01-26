from django.urls import reverse
from news.tests_.test_news_base import NewsBaseTest
from django.contrib.auth.models import User
from utils.testMixin.tests import TestMixin


class NewsCreateTest(NewsBaseTest):
    def setUp(self):
        self.view = reverse('news:index')

    def test_if_the_title_of_a_new_news_is_published(self):
        # Criar uma notícia
        news = self.create_news(is_published=True)

        # Http response | status code e várias outras coisas...
        response = self.client.get(self.view)

        # Pegar o HTML da página | converter para utf-8
        content = response.content.decode('utf-8')

        # Testar se o título da notícia está publicado
        self.assertIn(news.title, content)

    def test_if_the_description_of_a_new_news_is_published(self):
        # Criar uma notícia
        news = self.create_news(is_published=True)

        # Http response | status code e várias outras coisas...
        response = self.client.get(self.view)

        # Pegar o HTML da página | converter para utf-8
        content = response.content.decode('utf-8')

        # Testar se a descrição da notícia está publicado
        self.assertIn(news.description, content)

    def test_if_the_date_of_a_new_news_is_published(self):
        # Criar uma notícia
        self.create_news(is_published=True)

        # Http response | status code e várias outras coisas...
        response = self.client.get(self.view)

        # Pegar o HTML da página | converter para utf-8
        content = response.content.decode('utf-8')

        # Testar se a data da notícia está publicado
        self.assertIn('agora', content)

    def test_if_a_news_with_is_published_false_is_not_published(self):
        # Criar uma notícia
        news = self.create_news(is_published=False)

        # Http response | status code e várias outras coisas...
        response = self.client.get(self.view)

        # Pegar o HTML da página | converter para utf-8
        content = response.content.decode('utf-8')

        # Testar se uma notícia não publicada está no site
        self.assertNotIn(news.title, content)

    def test_if_a_new_user_shows_in_template(self):
        # Criar um autor
        author = self.create_profile_and_user()

        # Http response | status code e várias outras coisas...
        response = self.client.get(self.view)

        # Pegar o HTML da página | converter para utf-8
        content = response.content.decode('utf-8')

        self.assertIn(f'{author.author.first_name} {author.author.last_name}', content)

    def test_if_shows_a_message_if_not_exists_a_news(self):
        # Http response | status code e várias outras coisas...
        response = self.client.get(self.view)

        # Pegar o HTML da página | converter para utf-8
        content = response.content.decode('utf-8')

        # Http response | status code e várias outras coisas...
        self.assertIn('Não há conteúdo no momento :(', content)

    def test_if_shows_a_message_case_any_user_be_registered(self):
        # Http response | status code e várias outras coisas...
        response = self.client.get(self.view)

        content = response.content.decode('utf-8')

        # Http response | status code e várias outras coisas...
        self.assertIn('Nenhum usuário cadastrado', content)


    def test_if_shows_a_message_case_any_post_from_community_be_created(self):
        # Http response | status code e várias outras coisas...
        response = self.client.get(self.view)

        # Pegar o HTML da página | converter para utf-8
        content = response.content.decode('utf-8')

        # Http response | status code e várias outras coisas...
        self.assertIn(
            'A comunidade anda um pouco quieta, tente voltar um pouco mais tarde', content)

    def test_if_your_first_name_and_last_name_show_in_navbar(self):
        # Criar um usuário
        author = self.create_profile_and_user()

        # Http response | status code e várias outras coisas...
        response = self.client.get(self.view)

        # Pegar o HTML da página | converter para utf-8
        content = response.content.decode('utf-8')

        # Http response | status code e várias outras coisas...
        self.assertIn(
            f'{author.author.first_name} {author.author.last_name}', content)





class NewsPostView(NewsBaseTest):
    def get_url_with_slug(self, slug):
        view = reverse('news:post_detail', kwargs={'slug': slug})
        return view

    def test_title_is_correct(self):
        # Criar uma notícia
        news = self.create_news(is_published=True)

        # Http response | status code e várias outras coisas...
        response = self.client.get(self.get_url_with_slug(news.slug))

        # Pegar o HTML da página | converter para utf-8
        content = response.content.decode('utf-8')

        self.assertIn(news.title, content)

    def test_description_is_correct(self):
        # Criar uma notícia
        news = self.create_news(is_published=True)

        # Http response | status code e várias outras coisas...
        response = self.client.get(self.get_url_with_slug(news.slug))

        # Pegar o HTML da página | converter para utf-8
        content = response.content.decode('utf-8')

        self.assertIn(news.description, content)

    def test_content_is_correct(self):
        # Criar uma notícia
        news = self.create_news(is_published=True)

        # Http response | status code e várias outras coisas...
        response = self.client.get(self.get_url_with_slug(news.slug))

        # Pegar o HTML da página | converter para utf-8
        content = response.content.decode('utf-8')

        self.assertIn(news.content, content)

    def test_author_is_correct(self):
        # Criar uma notícia
        news = self.create_news(is_published=True)

        # Pegar o autor da notícia
        author = User.objects.filter(id=news.author.id).first()

        # Http response | status code e várias outras coisas...
        response = self.client.get(self.get_url_with_slug(news.slug))

        # Pegar o HTML da página | converter para utf-8
        content = response.content.decode('utf-8')

        self.assertIn(f'{author.first_name} {author.last_name}', content)
