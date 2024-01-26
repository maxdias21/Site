from .test_news_base import NewsMixin
from rest_framework import test
from django.urls import reverse
from unittest.mock import patch


class NewsApiTest(test.APITestCase, NewsMixin):
    def get_jtw_access_login(self, username='username', password='password'):
        user_data = {
            'username': username,
            'password': password,
        }

        # Criar usuário
        user = self.create_user(username=username, password=password)

        # Pegar a url
        url = reverse('news:token_obtain_pair')

        response = self.client.post(url, {**user_data})

        return {
            'jwt_access_token': response.data.get('access'),
            'jwt_refresh_token': response.data.get('refresh'),
            'user': user
        }

    def test_news_api_list_returns_status_code_200(self):
        # Pegar a url
        url = reverse('news:news-api-list')

        # Http response | status code e várias outras coisas...
        response = self.client.get(url)

        self.assertEqual(response.status_code, 200)

        @patch('news.views_.api.classes.news_class_api.NewsApiPagination.page_size', new=5)
        def test_news_api_list_loads_correct_number_of_news(self):
            # Criar várias notícias
            wanted_news = 5
            self.create_many_news(qnt=wanted_news)

            # Pegar a url
            url = reverse('news:news-api-list')

            # Http response | status code e várias outras coisas...
            response = self.client.get(url)

            # Mostrar todas as notícias
            # Desativado, só pra fins de estudo
            # response.data.get('results')

            qtd_news_received = len(response.data.get('results'))

            self.assertEqual(wanted_news, qtd_news_received)

    def test_do_not_must_show_news_that_not_is_published(self):
        # Criar uma notícia
        self.create_news(is_published=False)

        # Pegar a url
        url = reverse('news:news-api-list')

        # Http response | status code e várias outras coisas...
        response = self.client.get(url)

        self.assertEqual(len(response.data.get('results')), 0)

    def test_news_api_list_user_must_send_jwt_token_to_create_news(self):
        # Pegar a url
        url = reverse('news:news-api-list')

        # Http response | status code e várias outras coisas...
        response = self.client.post(url)

        self.assertEqual(response.status_code, 401)

    def test_news_api_list_logged_user_can_create_a_news(self):
        data = {
            'author': 1,
            'title': 'Title',
            'description': 'Description',
            'content': 'My content',
        }

        # Chamar a função e pegar um dicionário jwt
        auth_data = self.get_jtw_access_login()

        # Pegar o token de acesso
        access_token = auth_data.get('jwt_access_token')

        # Pegar a url
        url = reverse('news:news-api-list')

        # Http response | status code e várias outras coisas...
        response = self.client.post(url, data=data, HTTP_AUTHORIZATION=f'Bearer {access_token}')

        self.assertEqual(response.status_code, 201)

    def test_news_api_list_logged_user_can_update_a_news(self):
        # Criar um usuário
        author = self.get_jtw_access_login(username='username2', password='password2')

        data = {
            'title': 'Title Patch',
            'description': 'Description Patch',
            'content': 'My content Patch',
        }

        # Criar uma notícia
        news = self.create_news(is_published=True)
        news.author = author.get('user')
        news.save()

        # Pegar a url
        url = reverse('news:news-api-detail', args=(news.id,))

        # Http response | status code e várias outras coisas...
        response = self.client.patch(url, data=data, HTTP_AUTHORIZATION=f'Bearer {author.get("jwt_access_token")}')

        self.assertEqual(response.data.get('title'), 'Title Patch')

    def test_news_api_list_logged_user_cannot_update_a_news_owned_by_another_user(self):
        # Criar um usuário
        author = self.get_jtw_access_login(username='username2', password='password2')

        data = {
            'title': 'Title Patch',
            'description': 'Description Patch',
            'content': 'My content Patch',
        }

        # Criar uma notícia
        news = self.create_news(is_published=True)
        news.author = author.get('user')
        news.save()

        another_user = self.get_jtw_access_login(username='Another user')

        # Pegar a url
        url = reverse('news:news-api-detail', args=(news.id,))

        # Http response | status code e várias outras coisas...
        response = self.client.patch(url, data=data, HTTP_AUTHORIZATION=f'Bearer {another_user.get("jwt_access_token")}')

        self.assertEqual(response.status_code, 403)
