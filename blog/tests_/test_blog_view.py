from django.urls import resolve, reverse
from .. import views_
from .base import BlogBase


class TestBlogClass(BlogBase):
    def test_read_one_post_func_is_correct(self):
        # Coleta algumas informações com base na url que passar | func, args, kwargs, url_name...
        view = resolve(reverse('blog:post_detail', args=(1,)))

        self.assertIs(views_.ReadBlogNews, view.func.view_class)

    def test_blog_create_func_is_correct(self):
        # Coleta algumas informações com base na url que passar | func, args, kwargs, url_name...
        view = resolve(reverse('blog:create_post'))

        self.assertIs(views_.BlogCreatePost, view.func.view_class)

    def test_blog_create_create_func_is_correct(self):
        # Coleta algumas informações com base na url que passar | func, args, kwargs, url_name...
        view = resolve(reverse('blog:create_post'))

        self.assertIs(views_.BlogCreatePost, view.func.view_class)

    def test_blog_all_users_func_is_correct(self):
        # Coleta algumas informações com base na url que passar | func, args, kwargs, url_name...
        view = resolve(reverse('blog:all_users'))

        self.assertIs(views_.AllUsers, view.func.view_class)

    def test_blog_all_posts_func_is_correct(self):
        # Coleta algumas informações com base na url que passar | func, args, kwargs, url_name...
        view = resolve(reverse('blog:all_posts'))

        self.assertIs(views_.AllPosts, view.func.view_class)

    def test_blog_search_func_is_correct(self):
        # Coleta algumas informações com base na url que passar | func, args, kwargs, url_name...
        view = resolve(reverse('blog:search'))

        self.assertIs(views_.Search, view.func.view_class)


class TestBlogTemplate(BlogBase):
    def test_read_one_post_template_is_correct(self):
        # Criar um post para ter o "id" 1
        post = self.create_post(image='image')

        # Pegar o HTML da página | converter para utf-8
        content = self.client.get(reverse('blog:post_detail', args=(post.slug,)))

        self.assertTemplateUsed(content, 'global/partials/read_post.html')

    def test_create_post_template_is_correct(self):
        # Pegar o HTML da página | converter para utf-8
        content = self.client.get(reverse('blog:create_post'))

        self.assertTemplateUsed(content, 'blog/create_post.html')

    def test_create_create_post_template_is_correct(self):
        # Pegar o HTML da página | converter para utf-8
        content = self.client.get(reverse('blog:create_post'))

        self.assertTemplateUsed(content, 'blog/create_post.html')

    def test_all_users_template_is_correct(self):
        # Pegar o HTML da página | converter para utf-8
        content = self.client.get(reverse('blog:all_users'))

        self.assertTemplateUsed(content, 'blog/all_users.html')

    def test_all_poststemplate_is_correct(self):
        # Pegar o HTML da página | converter para utf-8
        content = self.client.get(reverse('blog:all_posts'))

        self.assertTemplateUsed(content, 'blog/all_posts.html')

    def test_search_post_template_is_correct(self):
        # Pegar o HTML da página | converter para utf-8
        content = self.client.get(reverse('blog:search'))

        self.assertTemplateUsed(content, 'blog/search.html')


class TestBlogStatusCode(BlogBase):
    def test_post_status_code_is_correct(self):
        # Criar um post para ter o "id" 1
        post = self.create_post(image='image')

        # Coleta algumas informações com base na url que passar | func, args, kwargs, url_name...
        url = reverse('blog:post_detail', args=(post.slug,))

        # Pegar o HTML da página | converter para utf-8
        content = self.client.get(url)

        self.assertIs(content.status_code, 200)

    def test_create_post_status_code_is_correct(self):
        # Coleta algumas informações com base na url que passar | func, args, kwargs, url_name...
        url = reverse('blog:create_post')

        # Pegar o HTML da página | converter para utf-8
        content = self.client.get(url)

        self.assertIs(content.status_code, 200)

    def test_create_create_post_status_code_is_correct(self):
        # Coleta algumas informações com base na url que passar | func, args, kwargs, url_name...
        url = reverse('blog:create_create_post')

        # Pegar o HTML da página | converter para utf-8
        content = self.client.get(url)

        self.assertIs(content.status_code, 200)

    def test_all_posts_status_code_is_correct(self):
        # Coleta algumas informações com base na url que passar | func, args, kwargs, url_name...
        url = reverse('blog:all_posts')

        # Pegar o HTML da página | converter para utf-8
        content = self.client.get(url)

        self.assertIs(content.status_code, 200)

    def test_all_users_status_code_is_correct(self):
        # Coleta algumas informações com base na url que passar | func, args, kwargs, url_name...
        url = reverse('blog:all_users')

        # Pegar o HTML da página | converter para utf-8
        content = self.client.get(url)

        self.assertIs(content.status_code, 200)

    def test_search_status_code_is_correct(self):
        # Coleta algumas informações com base na url que passar | func, args, kwargs, url_name...
        url = reverse('blog:search')

        # Pegar o HTML da página | converter para utf-8
        content = self.client.get(url)

        self.assertIs(content.status_code, 200)


class TestBlogAppName(BlogBase):
    def setUp(self):
        super().setUp()
        self.app_name = 'blog'

    def test_post_one_news_app_name_is_correct(self):
        # Criar um post para ter o "id" 1
        post = self.create_post(image='image')

        # coleta algumas informações com base na url que passar | func, args, kwargs, url_name...
        view = resolve(reverse('blog:post_detail', args=(post.slug,)))

        self.assertIs(view.app_name, self.app_name)

    def test_create_post_app_name_is_correct(self):
        # coleta algumas informações com base na url que passar | func, args, kwargs, url_name...
        view = resolve(reverse('blog:create_post'))

        self.assertIs(view.app_name, self.app_name)

    def test_create_create_post_app_name_is_correct(self):
        # coleta algumas informações com base na url que passar | func, args, kwargs, url_name...
        view = resolve(reverse('blog:create_create_post'))

        self.assertIs(view.app_name, self.app_name)

    def test_all_users_app_name_is_correct(self):
        # coleta algumas informações com base na url que passar | func, args, kwargs, url_name...
        view = resolve(reverse('blog:all_users'))

        self.assertIs(view.app_name, self.app_name)

    def test_all_posts_app_name_is_correct(self):
        # coleta algumas informações com base na url que passar | func, args, kwargs, url_name...
        view = resolve(reverse('blog:all_posts'))

        self.assertIs(view.app_name, self.app_name)

    def test_search_app_name_is_correct(self):
        # coleta algumas informações com base na url que passar | func, args, kwargs, url_name...
        view = resolve(reverse('blog:search'))

        self.assertIs(view.app_name, self.app_name)
