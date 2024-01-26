from django.shortcuts import render, redirect
from django.views import View
from blog.models import Blog
from ..forms.profileForm import AuthorProfileForm
from ..models import AuthorRegister
from django.views.generic import DetailView
from django.contrib import messages
from django.urls import reverse


class AuthorProfileCreate(View):
    # Dispatch é responsável por retornar um http response (get/post)
    # Se o usuário não estiver logado, ele retorna para a página de criar conta
    def dispatch(self, request, *args, **kwargs):
        if not request.user.is_authenticated:
            messages.error(request, 'Não possui uma conta? Crie uma agora mesmo :)')
            return redirect('login:login_create')

        # Se o autor tiver um perfil, redirecionar para editar perfil
        if AuthorRegister.objects.filter(author=request.user):
            return redirect('news:index')

        return super().dispatch(request, *args, **kwargs)

    def get(self, request):
        # Pegar formulário + cache
        form = AuthorProfileForm(self.request.session.get('session_profile'))

        return render(request, 'authors/create_profile.html', {
            'form': form
        })

    def post(self, request):
        # Pegar o formulário
        form = AuthorProfileForm(self.request.POST)

        # Cache
        self.request.session['session_profile'] = self.request.POST

        # Se o formulário for válido, entra no "if"
        # Entrar não significa que vai logar, só que os campos foram preenchidos corretamente
        if form.is_valid():
            # Receber as informações do formulário
            # commit = False | para não salvar o formulário, pois vou personalizar alguns campos
            profile = form.save(commit=False)

            # Autor é o usuário que está logado
            profile.author = request.user

            # Ativar o usuário
            profile.is_active = True

            # Salvar
            profile.save()

            # Deletar sessão
            del self.request.session['session_profile']

            messages.success(request, 'Perfil criado com sucesso!')

            return redirect('login:profile')

        messages.error(request, 'Erro ao criar perfil, revise os campos e tente novamente')
        return redirect('login:profile_create')


class MyProfile(View):
    def setup(self, request, *args, **kwargs):
        super().setup(request, *args, **kwargs)

        # Se não existir usuário, ele entra no dispatch
        if not request.user.is_authenticated:
            return

        # Pegar perfil
        self.profile = AuthorRegister.objects.filter(author=request.user).select_related('author').first()

        # Pegar formulário
        self.form = AuthorProfileForm(data=request.POST or None,
                                      instance=self.profile,
                                      files=request.FILES or None)

    # Dispatch é responsável por retornar um http response (get/post)
    # Se o usuário não estiver logado, ele retorna para a página de criar conta
    def dispatch(self, request, *args, **kwargs):
        if not request.user.is_authenticated:
            messages.error(request, 'Não possui uma conta? Crie uma agora mesmo :)')
            return redirect('login:login_create')

        # Se o autor não tiver um perfil, redirecionar para criar um
        if not AuthorRegister.objects.filter(author=request.user):
            messages.info(request, 'Vamos criar um perfil para você')
            return redirect('login:profile_create')

        return super().dispatch(request, *args, **kwargs)


    def get(self, request):
        posts = Blog.objects.filter(author=request.user, is_published=True)

        return render(request, 'authors/my_profile.html', {
            'form': self.form,
            'form_action': reverse('login:profile'),
            'profile': self.profile,
            'posts': posts,
            'qnt_posts': len(posts)
        })

    def post(self, request):
        if self.form.is_valid():
            # Salvar formulário
            self.form.save()

            messages.success(request, 'Perfil editado com sucesso!')
            return redirect('login:profile')

        messages.error(request,
                       'Falha ao salvar alterações, existem erros no formulário, tente novamente')
        return redirect('login:profile')


class AuthorsProfileView(DetailView):
    model = AuthorRegister
    template_name = 'authors/author_profile.html'
    context_object_name = 'author'

    def dispatch(self, request, *args, **kwargs):
        user = self.get_queryset().first()

        if user.author == self.request.user:
            messages.info(request, 'Você está vendo seu perfil agora')
            return redirect('login:profile')

        if user.profile_status == 'Privado':
            messages.error(request, 'Perfil privado')
            return redirect('blog:all_users')

        if not user:
            messages.error(request, 'Perfil privado')
            return redirect('blog:all_users')

        return super().dispatch(request, *args, **kwargs)

    def get_queryset(self):
        qs = super().get_queryset()
        qs = qs.filter(is_active=True, slug=self.kwargs.get('slug')).select_related('author')

        return qs

    def get_context_data(self, **kwargs):
        cd = super().get_context_data(**kwargs)

        # Pegar usuário
        user = self.get_queryset().first()

        # Pegar posts do usuário
        cd['posts'] = Blog.objects.filter(author=user.author)
        return cd
