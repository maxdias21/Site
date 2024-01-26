from django.urls import resolve, reverse
from .. import views_
from django.test import TestCase
from utils.testMixin.tests import TestMixin


class TestBlogClass(TestCase, TestMixin):
    def test_login_func_is_correct(self):
        # Coleta algumas informações com base na url que passar | func, args, kwargs, url_name...
        view = resolve(reverse('login:login'))

        self.assertIs(views_.Login, view.func.view_class)

    def test_login_create_func_is_correct(self):
        # Coleta algumas informações com base na url que passar | func, args, kwargs, url_name...
        view = resolve(reverse('login:login_create'))

        self.assertIs(views_.Login, view.func.view_class)

    def test_create_account_func_is_correct(self):
        # Coleta algumas informações com base na url que passar | func, args, kwargs, url_name...
        view = resolve(reverse('login:register'))

        self.assertIs(views_.CreateUser, view.func.view_class)

    def test_register_create_func_is_correct(self):
        # Coleta algumas informações com base na url que passar | func, args, kwargs, url_name...
        view = resolve(reverse('login:register_create'))

        self.assertIs(views_.CreateUser, view.func.view_class)

    def test_logout_func_is_correct(self):
        # Coleta algumas informações com base na url que passar | func, args, kwargs, url_name...
        view = resolve(reverse('login:logout'))

        self.assertIs(views_.Logout, view.func.view_class)

    def test_myprofile_func_is_correct(self):
        # Coleta algumas informações com base na url que passar | func, args, kwargs, url_name...
        view = resolve(reverse('login:profile'))

        self.assertIs(views_.MyProfile, view.func.view_class)

    def test_profile_create_func_is_correct(self):
        # Coleta algumas informações com base na url que passar | func, args, kwargs, url_name...
        view = resolve(reverse('login:profile_create'))

        self.assertIs(views_.AuthorProfileCreate, view.func.view_class)

    def test_profile_create_create_func_is_correct(self):
        # Coleta algumas informações com base na url que passar | func, args, kwargs, url_name...
        view = resolve(reverse('login:profile_create_create'))

        self.assertIs(views_.AuthorProfileCreate, view.func.view_class)

    def test_author_profile_view_func_is_correct(self):
        user = self.create_profile_and_user()

        # Coleta algumas informações com base na url que passar | func, args, kwargs, url_name...
        view = resolve(reverse('login:author_profile_view', args=(user.slug,)))

        self.assertIs(views_.AuthorsProfileView, view.func.view_class)


class TestBlogTemplate(TestCase, TestMixin):
    def test_login_template_is_correct(self):
        # Pegar o HTML da página | converter para utf-8
        content = self.client.get(reverse('login:login'))

        self.assertTemplateUsed(content, 'authors/login_user.html')

    def test_login_create_template_is_correct(self):
        # Pegar o HTML da página | converter para utf-8
        content = self.client.get(reverse('login:login_create'))

        self.assertTemplateUsed(content, 'authors/login_user.html')

    def test_create_account_template_is_correct(self):
        # Pegar o HTML da página | converter para utf-8
        content = self.client.get(reverse('login:register'))

        self.assertTemplateUsed(content, 'authors/create_user.html')

    def test_create_account_create_template_is_correct(self):
        # Pegar o HTML da página | converter para utf-8
        content = self.client.get(reverse('login:register_create'))

        self.assertTemplateUsed(content, 'authors/create_user.html')

    def test_logout_template_None(self):
        # Criar usuário + logar
        password = '123456'
        user = self.create_user(password=password)
        self.client.login(username=user, password=password)

        # Pegar o HTML da página | converter para utf-8
        content = self.client.post(reverse('login:logout'))
        print(content.__dict__)
        self.assertTemplateNotUsed(content)

    def test_all_posts_template_is_correct(self):
        # Pegar o HTML da página | converter para utf-8
        content = self.client.get(reverse('blog:all_posts'))

        self.assertTemplateUsed(content, 'blog/all_posts.html')

    def test_my_profile_template_is_correct(self):
        # Criar usuário + perfil + logar
        password = '123456'
        user = self.create_user(username='teste', password=password)
        self.create_profile_and_user(author=user)
        self.client.login(username=user, password=password)

        # Pegar o HTML da página | converter para utf-8
        content = self.client.get(reverse('login:profile'))

        self.assertTemplateUsed(content, 'authors/my_profile.html')

    def test_profile_create_is_correct(self):
        # Criar usuário + logar
        password = '123456'
        user = self.create_user(password=password)
        self.client.login(username=user, password=password)

        # Pegar o HTML da página | converter para utf-8
        content = self.client.get(reverse('login:profile_create'))

        self.assertTemplateUsed(content, 'authors/create_profile.html')

    def test_profile_create_create_is_correct(self):
        # Criar usuário + logar
        password = '123456'
        user = self.create_user(password=password)
        self.client.login(username=user, password=password)

        # Pegar o HTML da página | converter para utf-8
        content = self.client.get(reverse('login:profile_create_create'))

        self.assertTemplateUsed(content, 'authors/create_profile.html')

    def test_author_profile_view_is_correct(self):
        # Criar usuário + perfil + logar
        password = '123456'
        user = self.create_user(username='teste', password=password)
        self.create_profile_and_user(author=user)
        self.client.login(username=user, password=password)

        # Criar perfil de alguém
        new_author = self.create_profile_and_user()

        # Pegar o HTML da página | converter para utf-8
        content = self.client.get(reverse('login:author_profile_view', args=(new_author.slug,)))

        self.assertTemplateUsed(content, 'authors/author_profile.html')


class TestBlogStatusCode(TestCase, TestMixin):
    def test_login_status_code_is_correct(self):
        # Coleta algumas informações com base na url que passar | func, args, kwargs, url_name...
        url = reverse('login:login', )

        # Pegar o HTML da página | converter para utf-8
        content = self.client.get(url)

        self.assertEqual(content.status_code, 200)

    def test_login_create_status_code_is_correct(self):
        # Coleta algumas informações com base na url que passar | func, args, kwargs, url_name...
        url = reverse('login:login_create')

        # Pegar o HTML da página | converter para utf-8
        content = self.client.get(url)

        self.assertEqual(content.status_code, 200)

    def test_register_status_code_is_correct(self):
        # Coleta algumas informações com base na url que passar | func, args, kwargs, url_name...
        url = reverse('login:register')

        # Pegar o HTML da página | converter para utf-8
        content = self.client.get(url)

        self.assertEqual(content.status_code, 200)

    def test_register_create_status_code_is_correct(self):
        # Coleta algumas informações com base na url que passar | func, args, kwargs, url_name...
        url = reverse('login:register_create')

        # Pegar o HTML da página | converter para utf-8
        content = self.client.get(url)

        self.assertEqual(content.status_code, 200)

    def test_logout_status_code_is_correct(self):
        # Criar usuário + logar
        password = '123456'
        user = self.create_user(password=password)
        self.client.login(username=user, password=password)

        # Coleta algumas informações com base na url que passar | func, args, kwargs, url_name...
        url = reverse('login:logout')

        # Pegar o HTML da página | converter para utf-8
        content = self.client.post(url)

        self.assertEqual(content.status_code, 302)

    def test_my_profile_status_code_is_correct(self):
        # Criar usuário + perfil + logar
        password = '123456'
        user = self.create_user(password=password)
        author = self.create_profile_and_user(author=user)
        self.client.login(username=user, password=password)

        # Coleta algumas informações com base na url que passar | func, args, kwargs, url_name...
        url = reverse('login:profile')

        # Pegar o HTML da página | converter para utf-8
        content = self.client.get(url)

        self.assertEqual(content.status_code, 200)

    def test_profile_create_status_code_is_correct(self):
        # Criar usuário + perfil + logar
        password = '123456'
        user = self.create_user(password=password)
        self.client.login(username=user, password=password)

        # Coleta algumas informações com base na url que passar | func, args, kwargs, url_name...
        url = reverse('login:profile_create')

        # Pegar o HTML da página | converter para utf-8
        content = self.client.get(url)

        self.assertEqual(content.status_code, 200)

    def test_profile_create_create_status_code_is_correct(self):
        # Criar usuário + perfil + logar
        password = '123456'
        user = self.create_user(password=password)
        self.client.login(username=user, password=password)

        # Coleta algumas informações com base na url que passar | func, args, kwargs, url_name...
        url = reverse('login:profile_create')

        # Pegar o HTML da página | converter para utf-8
        content = self.client.get(url)

        self.assertEqual(content.status_code, 200)

    def test_author_profile_view_status_code_is_correct(self):
        # Criar usuário + perfil + logar
        password = '123456'
        user = self.create_user(password=password, username='teste22')
        self.client.login(username=user, password=password)
        self.create_profile_and_user(author=user)

        # Criar perfil da outra pessoa
        user2 = self.create_profile_and_user()

        # Coleta algumas informações com base na url que passar | func, args, kwargs, url_name...
        url = reverse('login:author_profile_view', args=(user2.author.username,))

        # Pegar o HTML da página | converter para utf-8
        content = self.client.get(url)

        self.assertEqual(content.status_code, 200)


class TestBlogAppName(TestCase):
    def setUp(self):
        super().setUp()
        self.app_name = 'login'

    def test_post_one_news_app_name_is_correct(self):
        # coleta algumas informações com base na url que passar | func, args, kwargs, url_name...
        view = resolve(reverse('login:login'))

        self.assertIs(view.app_name, self.app_name)

    def test_login_create_app_name_is_correct(self):
        # coleta algumas informações com base na url que passar | func, args, kwargs, url_name...
        view = resolve(reverse('login:login_create'))

        self.assertIs(view.app_name, self.app_name)

    def test_register_app_name_is_correct(self):
        # coleta algumas informações com base na url que passar | func, args, kwargs, url_name...
        view = resolve(reverse('login:register'))

        self.assertIs(view.app_name, self.app_name)

    def test_register_create_app_name_is_correct(self):
        # coleta algumas informações com base na url que passar | func, args, kwargs, url_name...
        view = resolve(reverse('login:register_create'))

        self.assertIs(view.app_name, self.app_name)

    def test_logout_app_name_is_correct(self):
        # coleta algumas informações com base na url que passar | func, args, kwargs, url_name...
        view = resolve(reverse('login:logout'))

        self.assertIs(view.app_name, self.app_name)

    def test_profile_app_name_is_correct(self):
        # coleta algumas informações com base na url que passar | func, args, kwargs, url_name...
        view = resolve(reverse('login:profile'))

        self.assertIs(view.app_name, self.app_name)


    def test_profile_create_app_name_is_correct(self):
        # coleta algumas informações com base na url que passar | func, args, kwargs, url_name...
        view = resolve(reverse('login:profile_create'))

        self.assertIs(view.app_name, self.app_name)

    def test_profile_create_create_app_name_is_correct(self):
        # coleta algumas informações com base na url que passar | func, args, kwargs, url_name...
        view = resolve(reverse('login:profile_create_create'))

        self.assertIs(view.app_name, self.app_name)

    def test_author_profile_view_app_name_is_correct(self):
        # coleta algumas informações com base na url que passar | func, args, kwargs, url_name...
        view = resolve(reverse('login:author_profile_view', args=(1,)))

        self.assertIs(view.app_name, self.app_name)
