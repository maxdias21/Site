from django.test import TestCase
from ..forms.profileForm import AuthorProfileForm
from unittest import skip
from django.contrib.auth.models import User
from django.urls import reverse
from utils.testMixin.tests import TestMixin


class AuthorsProfile(TestCase, TestMixin):
    def setUp(self):
        # Senha
        self.password = 'pass123456'

        # Criar perfil
        self.profile = self.create_profile_and_user()

        # Pegar usuário
        self.user = User.objects.filter(username=self.profile.author).first()

        return super().setUp()

    @skip('Nenhum campo possui placeholder')
    def test_field_placeholder_is_correct(self):
        # Pegar formulário para testar os placeholders
        form = AuthorProfileForm()

        # Placeholder dos campos
        fields = {
            'marital_status': '',
            'age': '',
            'hometown': '',
            'current_city': '',
            'phone_number': '',
            'description': '',
        }

        for key in fields.items():
            with self.subTest(key):
                placeholder = form[key[0]].field.widget.attrs['placeholder']
                self.assertEqual(key[1], placeholder)

    @skip('Nenhum campo possui help text')
    def test_field_help_text_is_correct(self):
        # Pegar formulário para testar help text
        form = AuthorProfileForm()

        # Help text dos campos
        fields = {
            'marital_status': '',
            'age': '',
            'hometown': '',
            'current_city': '',
            'phone_number': '',
            'description': '',
        }

        for key in fields.items():
            with self.subTest(key):
                help_text = form[key[0]].field.help_text
                self.assertEqual(key[1], help_text)

    def test_field_label_is_correct(self):
        # Pegar formulário para testar label
        form = AuthorProfileForm()

        # label dos campos
        fields = {
            'marital_status': 'Estado civil',
            'age': 'Idade',
            'hometown': 'Cidade natal',
            'current_city': 'Cidade atual',
            'phone_number': 'Número de telefone',
            'description': 'Descrição do perfil',
        }

        for key in fields.items():
            with self.subTest(key):
                label = form[key[0]].label
                self.assertEqual(label, key[1])

    def test_user_not_has_posts_shows_a_message(self):
        # Logar usuário
        self.client.login(username=self.user.username, password=self.password)

        # Http response | status code e várias outras coisas...
        response = self.client.get(reverse('login:profile'), follow=True)

        # Pegar o HTML da página | converter para utf-8
        content = response.content.decode('utf=8')

        self.assertIn('Você não publicou nada ainda', content)

    def test_status_profile_shows_exactly_on_template(self):
        # Logar usuário
        self.client.login(username=self.user.username, password=self.password)

        # Http response | status code e várias outras coisas...
        response = self.client.get(reverse('login:profile'), follow=True)

        # Pegar o HTML da página | converter para utf-8
        content = response.content.decode('utf=8')

        self.assertIn('Público', content)

    def test_username_shows_exactly_on_template(self):
        # Logar usuário
        self.client.login(username=self.user.username, password=self.password)

        # Http response | status code e várias outras coisas...
        response = self.client.get(reverse('login:profile'), follow=True)

        # Pegar o HTML da página | converter para utf-8
        content = response.content.decode('utf=8')

        self.assertIn(str(self.user.username), content)



class AuthorProfileFormIntegrationTest(TestCase):
    def setUp(self):
        self.password = 'Password123'

        # Criar um usuário
        self._user = User.objects.create_user(first_name='First', last_name='Last', username='teste123',
                                              email='teste@gmail.com', password=self.password)

        # Criar um formulário
        self.form_data = {
            'age': '20',
            'hometown': 'Hometown',
            'current_city': 'Current_city',
            'marital_status': 'Solteiro',
            'phone_number': '11111111111',
            'description': 'My description',
            'photo': 'MyPhoto',
            'profile_status': 'Privado'
        }

        return super().setUp()

    def test_errors_empty_field(self):
        # Logar o usuário
        self.client.login(username=self._user.username, password=self.password)

        # Transformar os campos em vazios
        # Pegar os erros dos campos vazios
        self.form_data = {
            'hometown': '',
            'age': '',
            'current_city': '',
            'marital_status': '',
            'phone_number': '',
            'description': '',
            'photo': '',
            'profile_status': '',
        }
        print(self.form_data)
        # Pegar os erros dos campos vazios
        form_data = {
            'hometown': 'Digite sua cidade natal',
            'age': 'Digite sua idade',
            'current_city': 'Digite o estado no qual você mora atualmente',
            'marital_status': '',
            'phone_number': 'Digite seu número de telefone',
            'description': 'Digite uma breve descrição sobre sua vida ou algo que você goste',
            'photo': '',
            'profile_status': 'Seu perfil vai ser público ou privado?',
        }

        # Pegar a url
        url = reverse('login:profile_create')

        # Http response | status code e várias outras coisas...
        response = self.client.post(url, data={}, follow=True)

        # Pegar o HTML da página | converter para utf-8
        content = response.content.decode('utf-8')

        for key in form_data.items():
            self.assertIn(key[1], content)
