from .base import BlogBase
from django.urls import reverse


class CreatePostBlog(BlogBase):
    def create_many_posts(self, author, qnt=1):
        for post in range(0, qnt + 1):
            self.create_post(author=author,
                             title=f'This is my title {str(post)}',
                             content=f'This is my content {str(post)}',
                             description=f'This is my description {str(post)}',
                             image='',
                             slug=str(post))

    def test_post_create_is_correct(self):
        # Pegar url
        url = reverse('blog:create_post')

        # Criar usuário
        password = '123456'
        user = self.create_user(password=password)

        # Logar usuário
        self.client.login(username=user, password=password)

        # Http response | status code e várias outras coisas...
        response = self.client.post(url, data=self.form_data_create_post, follow=True)

        # Pegar o HTML da página | converter para utf-8
        content = response.content.decode('utf-8')

        self.assertIn('Seu post foi criado e logo será publicado', content)

    def test_post_create_is_wrong(self):
        # Pegar url
        url = reverse('blog:create_post')

        self.form_data_create_post = {
            'title': 'Tit',
            'description': 'Description',
            'content': 'Content',
            'image': ''
        }

        # Criar usuário
        password = '123456'
        user = self.create_user(password=password)

        # Logar usuário
        self.client.login(username=user, password=password)

        # Http response | status code e várias outras coisas...
        response = self.client.post(url, data=self.form_data_create_post, follow=True)

        # Pegar o HTML da página | converter para utf-8
        content = response.content.decode('utf-8')

        self.assertIn('Erro ao criar o seu post! Revise todos os campos e tente novamente', content)

    def test_create_many_post_and_must_show_on_template(self):
        # Quantidade de notícias
        qnt = 5

        # Criar usuário
        password = '123456'
        user = self.create_user(password=password)

        # Logar usuário
        self.client.login(username=user, password=password)

        # Criar vários posts
        self.create_many_posts(user, qnt)

        # Pegar url
        url = reverse('blog:all_posts')

        # Http response | status code e várias outras coisas...
        response = self.client.get(url)

        # Pegar o HTML da página | converter para utf-8
        content = response.content.decode('utf-8')

        with self.subTest():
            for x in range(0, qnt + 1):
                self.assertIn(f'This is my title {str(x)}', content)
                self.assertIn(f'This is my description {str(x)}', content)

    def test_create_one_user_and_shows_on_template(self):
        # Criar usuário
        password = '123456'
        user = self.create_user(password=password)

        # Logar usuário
        self.client.login(username=user, password=password)

        # Pegar url
        url = reverse('blog:all_users')

        # Http response | status code e várias outras coisas...
        response = self.client.get(url)

        # Pegar o HTML da página | converter para utf-8
        content = response.content.decode('utf-8')

        self.assertIn(user.first_name, content)
