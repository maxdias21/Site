from django.shortcuts import render, redirect
from django.views import View
from ..forms.blog_create import BlogCreateForm
from django.contrib import messages
from django.urls import reverse
from utils.views.authenticated import NotAuthenticated


class BlogCreatePost(NotAuthenticated):
    def get(self, request):
        # Pegar formulário
        form = BlogCreateForm(self.request.session.get('session_create_blog_post'))

        return render(request, 'blog/create_post.html', {
            'form': form,
            'form_action': reverse('blog:create_create_post')
        })

    def post(self, request):
        # Pegar formulário
        form = BlogCreateForm(data=self.request.POST or None, files=self.request.FILES or None)

        # Criar cache
        request.session['session_create_blog_post'] = self.request.POST

        if form.is_valid():
            # Receber as informações do formulário
            # commit = False | para não salvar o formulário, pois vou personalizar alguns campos
            profile = form.save(commit=False)

            # Cadastrar autor do post
            profile.author = request.user

            # Salvar post
            profile.save()

            # Mensagem sucesso + redirecionar + apagar cache
            messages.success(request, 'Seu post foi criado e logo será publicado')
            del request.session['session_create_blog_post']
            return redirect('login:profile')

        messages.error(request, 'Erro ao criar o seu post! Revise todos os campos e tente novamente')
        return redirect('blog:create_post')
