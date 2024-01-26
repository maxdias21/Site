from django.forms import ModelForm
from ..models import Blog
from utils.django_forms import add_label
from collections import defaultdict
from django.core.exceptions import ValidationError


class BlogCreateForm(ModelForm):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        # Pegar campos
        title = self.fields['title']
        description = self.fields['description']
        content = self.fields['content']
        image = self.fields['image']

        # Adicionar labels
        add_label(title, 'Título')
        add_label(description, 'Descrição')
        add_label(content, 'Conteúdo')
        add_label(image, 'Imagem')

        # Personalizar error_messages
        title.error_messages = {
            'required': 'Por favor, digite o título do seu post',
            'max_length': 'Máximo de caracteres permitidos é 100',
        }

        description.error_messages = {
            'required': 'Por favor, digite a descrição do seu post',
            'max_length': 'Máximo de caracteres permitidos é 250',
        }

        content.error_messages = {
            'required': 'Por favor, digite o conteúdo principal do seu post',
            'max_length': 'Máximo de caracteres permitidos é 2000',
        }

        image.error_messages = {
            'required': 'Campo obrigatório',
        }

    class Meta:
        model = Blog
        fields = ['title', 'description', 'content', 'image']

    def clean(self):
        # Dicionário para salvar os errors
        errors = defaultdict(list)

        # Pegar todos os campos
        fields = self.cleaned_data

        if (len(fields['title']) < 5):
            errors['title'].append('Esse campo deve conter no mínimo 5 caracteres')

        if (len(fields['description']) < 5):
            errors['description'].append('Esse campo deve conter no mínimo 5 caracteres')

        if (len(fields['content']) < 5):
            errors['content'].append('Esse campo deve conter no mínimo 5 caracteres')

        if errors:
            raise ValidationError(errors)
