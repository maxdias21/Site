from django.contrib.auth.models import User
from django.core.exceptions import ValidationError
from django import forms
from collections import defaultdict


class UserForm(forms.ModelForm):
    # Criação dos campos do formulário
    first_name = forms.CharField(required=True,
                                 max_length=255, min_length=1,
                                 label='Nome',
                                 error_messages={
                                     'required': 'Digite seu nome',
                                     'max_length': 'Máximo de caracteres permitido é 255',
                                     'min_length': 'Nome deve conter 1 caracteres ou mais',
                                 })

    last_name = forms.CharField(required=True,
                                max_length=255, min_length=1,
                                label='Sobrenome',
                                error_messages={
                                    'required': 'Digite seu sobrenome',
                                    'max_length': 'Máximo de caracteres permitido é 255',
                                    'min_length': 'Sobrenome deve conter 1 caracteres ou mais',
                                })

    email = forms.EmailField(required=True,
                             max_length=20, min_length=4,
                             label='Email',
                             error_messages={
                                 'required': 'Digite um email válido',
                                 'max_length': 'Máximo de caracteres permitido é 255',
                             },
                             help_text='Email não poderá ser alterado futuramente'
                             )

    username = forms.CharField(required=True,
                               max_length=20, min_length=4,
                               label='Usuário',
                               error_messages={
                                   'required': 'Digite um usuário válido',
                                   'max_length': 'Máximo de caracteres permitido é 20',
                                   'min_length': 'Usuário deve conter 4 caracteres ou mais',
                               },
                               help_text='Usuário não poderá ser alterado futuramente'
                               )

    password = forms.CharField(required=True,
                               max_length=20, min_length=4,
                               label='Senha',
                               error_messages={
                                   'required': 'Digite um usuário válido',
                                   'max_length': 'Máximo de caracteres permitido é 20',
                                   'min_length': 'Usuário deve conter 4 caracteres ou mais',
                               },
                               widget=forms.PasswordInput()
                               )

    password2 = forms.CharField(required=True,
                                max_length=20, min_length=4,
                                label='Repetir senha',
                                error_messages={
                                    'required': 'Digite uma senha válida',
                                    'max_length': 'Máximo de caracteres permitido é 255',
                                    'min_length': 'Senha deve conter 6 caracteres ou mais',
                                },
                                widget=forms.PasswordInput()
                                )

    class Meta:
        model = User
        fields = ['first_name', 'last_name', 'username', 'email', 'password']

    def clean(self):
        # Criar um dicionário que contém dicionários
        # Toda vez que eu usar isso ele cria um dicionário com uma lista
        # Envio todos os erros ao invés de ficar a colocar raise ValidationError para cada campo individual
        errors = defaultdict(list)

        # Pegar campo email
        email = self.cleaned_data['email']

        # Verificar se email já foi cadastrado
        email_exists = User.objects.filter(email=email).exists()

        # Usuário cadastrado = erro
        if email_exists:
            errors['email'].append('Email já existe')

        # Pegar campo usuário
        username = self.cleaned_data['username']

        # Verificar se usuário já foi cadastrado
        username_exists = User.objects.filter(username=username).exists()

        # Usuário cadastrado = erro
        if username_exists:
            errors['username'].append('Usuário já existe')

        # Pegar campos das senhas
        password = self.cleaned_data['password']
        password2 = self.cleaned_data['password2']

        if password != password2:
            errors['password'].append('Senhas não coincidem')
            errors['password2'].append('Senhas não coincidem')

        if errors:
            raise ValidationError(errors)
