from django.contrib import messages
from authors.forms.userForm import UserForm
from django.shortcuts import render, redirect
from django.views import View
from django.urls import reverse
from utils.views.authenticated import IsAuthenticated

class CreateUser(IsAuthenticated):
    def get(self, request):
        # Pegar formulário + cache para não perder os dados caso envie o form errado
        form = UserForm(self.request.session.get('session_register'))

        return render(request, 'authors/create_user.html', {
            'form': form,
            'form_action': reverse('login:register_create')
        })

    def post(self, request):
        # Pegar o formulário
        form = UserForm(request.POST)

        # Cache
        request.session['session_register'] = request.POST

        # Se o formulário for válido, entra no "if"
        # Entrar não significa que vai logar, só que os campos foram preenchidos corretamente
        if form.is_valid():
            # Receber as informações do formulário
            # commit = False | para não salvar o formulário, pois vou personalizar alguns campos
            user = form.save(commit=False)

            # Fazer hash da senha
            user.set_password(user.password)

            user.save()

            messages.success(request, 'Usuário criado com sucesso!')

            # Deletar o cache | redirecionar para a página de login
            del self.request.session['session_register']
            return redirect('login:login')

        messages.error(request, 'Erro ao criar perfil, revise os campos abaixo')
        return redirect('login:register')