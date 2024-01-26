from django.urls import path, include
from . import views_
from rest_framework.routers import SimpleRouter
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView, TokenVerifyView

app_name = 'news'

# Configurar rotas
news_routes = SimpleRouter()
news_routes.register(
    'news/api/v1',
    views_.NewsApiViewSet,
    basename='news-api'
)

urlpatterns = [
    # Rota inicial do site
    path('', views_.NewsIndex.as_view(), name='index'),
    # Todas as notícias
    path('news/all/', views_.AllNews.as_view(), name='all_news'),
    # Ler uma notícia
    path('news/<slug:slug>/', views_.ReadNews.as_view(), name='post_detail'),
    # Filtrar notícia por tag
    path('news/tag/<slug:slug>/', views_.Tags.as_view(), name='tags'),
]

# Api com classes
urlpatterns += [
    # Para usar junto com "ModelViewSet", desativado por usar simple route
    # Faz tudo que tiver dentro do dict
    # path('news/api/v1/', views_.NewsApiViewSet.as_view(
    #   {
    #      'get': 'list',
    #     'post': 'create',
    # }
    # ), name = 'api_all_news'),
    #
    # Faz tudo que tiver dentro do dict
    # path('news/api/v1/<int:pk>/', views_.NewsApiViewSet.as_view({
    #   'get': 'retrieve',
    #  'patch': 'partial_update',
    # 'delete': 'destroy'
    # }
    # ), name='api_news_detail'),

    # Link do hyperlink da tag
    path('news/api/tag/<int:pk>/', views_.TagApiDetail.as_view(), name='api_news_tag'),
    # Api Token
    # Obter token
    path('news/api/token/', TokenObtainPairView.as_view(),name='token_obtain_pair'),
    # Atualizar token
    path('news/api/token/refresh/', TokenRefreshView.as_view(),name='token_refresh_pair'),
    # Verificar token
    path('news/api/token/verify/', TokenVerifyView.as_view(),name='token_verify_pair'),

    # Sempre no final
    path('', include(news_routes.urls))
]

# Api com funções
"""urlpatterns += [
    # Pegar todas as notícias
    path('news/api/all_news/', views_.api_all_news, name='api_all_news'),
    # Pegar uma notícia
    path('news/api/<int:pk>/', views_.api_get_one_news, name='api_view_detail'),
    # Link do hyperlink da tag
    path('news/api/tag/<int:pk>/', views_.api_tag_api_detail, name='api_news_tag'),
]
"""
