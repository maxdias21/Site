from django.test import TestCase
from utils.testMixin.tests import TestMixin
from django.urls import reverse


class LoginTest(TestCase, TestMixin):
    def test_user_tries_to_logout_using_method_get(self) -> None:
        # Criar senha
        password = '123456'

        # Criar usuário
        user = self.create_user(password=password)

        # Logar usuário
        self.client.login(username=user.username, password=password)

        # Http response | status code e várias outras coisas...
        response = self.client.get(reverse('login:logout'), follow=True)

        # Pegar o HTML da página | converter para utf-8
        content = response.content.decode('utf-8')

        self.assertIn('Erro ao sair da conta', content)

    def test_user_triest_to_logout_another_user(self):
        # Criar senha
        password = '123456'

        # Criar usuário
        user = self.create_user(password=password)

        # Logar usuário
        self.client.login(username=user.username, password=password)

        response = self.client.get(reverse('login:logout'), follow=True, data={'username': 'User2'})

        # Pegar o HTML da página | converter para utf-8
        content = response.content.decode('utf-8')

        self.assertIn('Erro ao sair da conta', content)

    def test_user_can_login_successfully(self):
        password = 'Senha123'

        # Criar usuário
        user = self.create_user(password=password)

        # Http response | status code e várias outras coisas...
        response = self.client.post(reverse('login:login_create'), follow=True,
                                    data={'username': user.username, 'password': password})

        # Pegar o HTML da página | converter para utf-8
        content = response.content.decode('utf-8')

        self.assertIn('Usuário logado com sucesso!', content)

    def test_user_can_logout_successfully(self):
        password = 'Senha123'

        # Criar usuário
        user = self.create_user(password=password)

        # Logar usuário
        self.client.login(username=user.username, password=password)

        # Http response | status code e várias outras coisas...
        response = self.client.post(reverse('login:logout'), follow=True,
                                    data={'username': str(user.username)})

        # Pegar o HTML da página | converter para utf-8
        content = response.content.decode('utf-8')

        self.assertIn('Você saiu da sua conta com sucesso!', content)
