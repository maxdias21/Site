from django.urls import path
from . import views_

app_name = 'blog'

urlpatterns = [
    # Ler notícia do blog
    path('<slug:slug>/', views_.ReadBlogNews.as_view(), name='post_detail'),
    # Criar post
    path('create/post/', views_.BlogCreatePost.as_view(), name='create_post'),
    path('create/create/post/', views_.BlogCreatePost.as_view(), name='create_create_post'),
    # Ver todos os usuários
    path('all/users/', views_.AllUsers.as_view(), name='all_users'),
    # Ver todos os posts
    path('all/posts/', views_.AllPosts.as_view(), name='all_posts'),
    # Pesquisar sobre tudo
    path('all/search/', views_.Search.as_view(), name='search')
]
