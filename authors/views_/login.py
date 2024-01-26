from django.shortcuts import render, redirect
from django.views import View
from authors.forms.loginForm import LoginForm
from django.contrib import messages
from django.urls import reverse
from django.contrib.auth import login, authenticate
from utils.views.authenticated import IsAuthenticated

class Login(IsAuthenticated):
    def get(self, request):
        # Pegar formulário + cache para não perder os dados caso envie o form errado
        form = LoginForm(request.session.get('login_session'))

        return render(request=request, template_name='authors/login_user.html', context={
            'form': form,
            'form_action': reverse('login:login_create')
        })

    def post(self, request):
        # Pegar o formulário
        form = LoginForm(request.POST)

        # Cache
        request.session['login_session'] = request.POST

        # Se o formulário for válido, entra no "if"
        # Entrar não significa que vai logar, só que os campos foram preenchidos corretamente
        if form.is_valid():
            # Vou autenticar o usuário | retorna o nome do usuário ou None
            authenticate_user = authenticate(
                username=form.cleaned_data.get('username', ''),
                password=form.cleaned_data.get('password', '')
            )

            # Se entrar no "if" vai logar o usuário
            if authenticate_user:
                messages.success(self.request, 'Usuário logado com sucesso!')
                login(self.request, authenticate_user)

                # Apagar sessão
                del request.session['login_session']

                return redirect(reverse('news:index'))
            else:
                # Usuário digitou algo errado ou a conta não existe
                messages.error(self.request, 'Senha incorreta ou usuário não existe, verifique suas credenciais!')
        else:
            messages.error(self.request, 'Erro ao enviar o formulário')

        return redirect(reverse('login:login'))