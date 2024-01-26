from .browser import make_chrome_browser
from django.contrib.staticfiles.testing import StaticLiveServerTestCase
from selenium.webdriver.common.by import By
from django.contrib.auth.models import User


class AuthorBaseTest(StaticLiveServerTestCase):
    # Primeira coisa a ser executada
    # Cria a base do selenium
    def setUp(self):
        self.browser = make_chrome_browser()

        return super().setUp()

    # Última coisa a ser executada
    # Fecha o navegador
    def tearDown(self):
        self.browser.quit()

    def user_create(self, first_name='First', last_name='Last', username='username', email='email@gmail.com',
                    password='pass123456'):
        return User.objects.create_user(first_name=first_name, last_name=last_name, username=username, email=email,
                                        password=password)

    def get_by_placeholder(self, web_element, placeholder: str):
        return web_element.find_element(By.XPATH, f'\\input[@placeholder={placeholder}]')
