from django.urls import path, include
from rest_framework.routers import SimpleRouter
from . import views_

app_name = 'login'

# Configurar rotas
author_routes = SimpleRouter()
author_routes.register(
    'api/v1',
    views_.AuthorViewSet,
    basename='author-api'
)

urlpatterns = [
    # Página de login
    path('', views_.Login.as_view(), name='login'),
    path('login/create/', views_.Login.as_view(), name='login_create'),
    # Página de cadastro
    path('create/account/', views_.CreateUser.as_view(), name='register'),
    path('create/create/account/', views_.CreateUser.as_view(), name='register_create'),
    # Logout
    path('logout/', views_.Logout.as_view(), name='logout'),
    # Perfil do usuário
    path('myprofile/', views_.MyProfile.as_view(), name='profile'),
    path('profile/create/', views_.AuthorProfileCreate.as_view(), name='profile_create'),
    path('profile/create/create/', views_.AuthorProfileCreate.as_view(), name='profile_create_create'),
    # Ver perfil de alguém
    path('profile/<slug:slug>/', views_.AuthorsProfileView.as_view(), name='author_profile_view'),
    # Sempre no final
    path('', include(author_routes.urls))
]

