from .base import AuthorBaseTest
from selenium.webdriver.common.by import By
from django.urls import reverse
from time import sleep


class AuthorLoginTest(AuthorBaseTest):
    def test_user_valid_data_can_login_successfully(self):
        password = 'Pass123'

        # Url inicial
        self.browser.get(self.live_server_url + reverse('login:login'))
        sleep(2)

        # Criar usuário
        user = self.user_create(password=password)

        # Selecionar formulário
        form = self.browser.find_element(By.CSS_SELECTOR, '#login > div > div > div > div > form')

        # Selecionar input username | enviar dados para o campo username
        username_field = form.find_element(By.ID, 'id_username')
        username_field.send_keys(str(user.username))

        # Selecionar input username | enviar dados para o campo password
        password_field = form.find_element(By.ID, 'id_password')
        password_field.send_keys(password)

        # Clicar no botão que contém o type submit
        form.submit()

        # A página mudou quando clicou em "form.submit()", pegar formulário novamente
        form = self.browser.find_element(By.TAG_NAME, 'body').text

        self.assertIn('Usuário logado com sucesso!', form)

    def test_login_form_invalid_credentials(self):
        # Url inicial
        self.browser.get(self.live_server_url + reverse('login:login'))

        # Selecionar formulário
        form = self.browser.find_element(By.CSS_SELECTOR, '#login > div > div > div > div > form')

        # Selecionar input username | enviar dados para o campo username
        username_field = form.find_element(By.ID, 'id_username')
        username_field.send_keys('NotFound')

        # Selecionar input username | enviar dados para o campo password
        password_field = form.find_element(By.ID, 'id_password')
        password_field.send_keys('NotFound')
        sleep(2)

        # Clicar no botão que contém o type submit
        form.submit()
        sleep(5)


        # A página mudou quando clicou em "form.submit()", pegar formulário novamente
        form = self.browser.find_element(By.TAG_NAME, 'body').text

        self.assertIn('Senha incorreta ou usuário não existe, verifique suas credenciais!', form)


    def test_login_form_is_invalid(self):
        # Url inicial
        self.browser.get(self.live_server_url + reverse('login:login'))

        # Selecionar formulário
        form = self.browser.find_element(By.CSS_SELECTOR, '#login > div > div > div > div > form')

        # Selecionar input username | enviar dados para o campo username
        username_field = form.find_element(By.ID, 'id_username')
        username_field.send_keys('')

        # Selecionar input username | enviar dados para o campo password
        password_field = form.find_element(By.ID, 'id_password')
        password_field.send_keys('')

        # Clicar no botão que contém o type submit
        form.submit()
        sleep(50)


        # A página mudou quando clicou em "form.submit()", pegar formulário novamente
        form = self.browser.find_element(By.TAG_NAME, 'body').text

        self.assertIn('Erro ao enviar o formulário', form)



