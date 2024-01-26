from django import forms
from utils.django_forms import add_label
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError


class LoginForm(forms.Form):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        # Pegar campos
        username = self.fields['username']
        password = self.fields['password']

        username.help_text = 'Seu nome de usuário deve conter apenas letras e números'

        # Adicionar error messages
        username.error_messages = {
            'required':'Esse campo é obrigatório'
        }

        password.error_messages = {
            'required': 'Esse campo é obrigatório'
        }

        # Adicionar label
        add_label(username, 'Usuário')
        add_label(password, 'Senha')

    # Campos
    username = forms.CharField(min_length=5, max_length=255)
    password = forms.CharField(widget=forms.PasswordInput(), min_length=6, max_length=255)


