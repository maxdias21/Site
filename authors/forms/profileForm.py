from django.forms import ModelForm
from ..models import AuthorRegister
from django.core.exceptions import ValidationError
from collections import defaultdict
from django import forms


class AuthorProfileForm(ModelForm):
    class Meta:
        model = AuthorRegister
        fields = ('age', 'hometown', 'current_city', 'marital_status',
                  'phone_number', 'description', 'photo', 'profile_status')

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        # Personalizar error_messages
        self.fields['hometown'].error_messages = {
            'required': 'Digite sua cidade natal'
        }

        self.fields['current_city'].error_messages = {
            'required': 'Digite o estado no qual você mora atualmente'
        }

        self.fields['description'].error_messages = {
            'required': 'Digite uma breve descrição sobre sua vida ou algo que você goste'
        }

        self.fields['profile_status'].error_messages = {
            'required': 'Seu perfil vai ser público ou privado?'
        }

    # Criação dos campos do formulário
    age = forms.IntegerField(required=True,
                             label='Idade',
                             error_messages={
                                 'required': 'Digite sua idade',
                                 'min_value': 'Digite uma idade válida',
                                 'max_value': 'Digite uma idade válida',
                             }, )

    # Criação dos campos do formulário
    phone_number = forms.CharField(required=True,
                                   max_length=11, min_length=11,
                                   label='Número de telefone',
                                   error_messages={
                                       'required': 'Digite seu número de telefone',
                                       'min_length': 'Número inválido, digite um número de telefone sem traços e pontos, apenas números',
                                       'max_length': 'Número inválido, digite um número de telefone sem traços e pontos, apenas números',
                                   })

    def clean(self):
        errors = defaultdict(list)
        cleaned_data = self.cleaned_data

        if not cleaned_data.get('phone_numer') and not cleaned_data.get('age') and not cleaned_data.get('description'):
            raise ValidationError('Erro desconhecido, tente novamente mais tarde')

        field_phone_number = cleaned_data['phone_number']
        field_age = cleaned_data['age']
        description = cleaned_data['description']

        if not field_phone_number.isnumeric():
            errors['phone_number'].append(
                'Número inválido, digite um número de telefone sem traços e pontos, apenas números')

        if field_age > 120:
            errors['age'].append('Digite uma idade válida')

        if len(description) < 5:
            errors['description'].append('Sua descrição deve conter no mínimo 5 caracteres')

        if errors:
            raise ValidationError(errors)
