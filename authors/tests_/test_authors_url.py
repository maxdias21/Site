from django.test import TestCase
from django.urls import reverse

class BlogNewsUrl(TestCase):
    def test_url_login_is_correct(self):
        # Http response | status code e várias outras coisas...
        url = reverse('login:login')

        self.assertEqual('/login/', url)

    def test_url_login_create_is_correct(self):
        # Http response | status code e várias outras coisas...
        url = reverse('login:login_create')

        self.assertEqual('/login/login/create/', url)

    def test_url_create_account_is_correct(self):
        # Http response | status code e várias outras coisas...
        url = reverse('login:register')

        self.assertEqual('/login/create/account/', url)

    def test_url_create_account_create_is_correct(self):
        # Http response | status code e várias outras coisas...
        url = reverse('login:register_create')

        self.assertEqual('/login/create/create/account/', url)

    def test_url_logout_is_correct(self):
        # Http response | status code e várias outras coisas...
        url = reverse('login:logout')

        self.assertEqual('/login/logout/', url)

    def test_url_myprofile_is_correct(self):
        # Http response | status code e várias outras coisas...
        url = reverse('login:profile')

        self.assertEqual('/login/myprofile/', url)

    def test_url_profile_create_is_correct(self):
        # Http response | status code e várias outras coisas...
        url = reverse('login:profile_create')

        self.assertEqual('/login/profile/create/', url)

    def test_url_profile_create_create_is_correct(self):
        # Http response | status code e várias outras coisas...
        url = reverse('login:profile_create_create')

        self.assertEqual('/login/profile/create/create/', url)

    def test_url_author_profile_is_correct(self):
        # Http response | status code e várias outras coisas...
        url = reverse('login:author_profile_view', args=(1,))

        self.assertEqual('/login/profile/1/', url)


