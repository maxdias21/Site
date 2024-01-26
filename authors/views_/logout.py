from django.contrib import messages
from django.views import View
from django.shortcuts import redirect
from django.contrib.auth import logout
from utils.views.authenticated import NotAuthenticated


class Logout(NotAuthenticated):
    def get(self, request):
        messages.error(request, 'Erro ao sair da conta')
        return redirect('news:index')

    def post(self, request):
        # Se tentar sair com um usuário diferente, vai dar erro
        if request.POST.get('username') != request.user.username:
            messages.error(request, 'Erro ao sair da conta')
            return redirect('news:index')

        # Logout
        messages.success(request, 'Você saiu da sua conta com sucesso!')
        logout(request)

        return redirect('login:login')
