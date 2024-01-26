from rest_framework import status
from rest_framework.views import APIView
from news.models import News
from ..serializer import NewsSerializer
from rest_framework.response import Response
from datetime import datetime
from django.utils.text import slugify
from rest_framework.generics import ListCreateAPIView
from rest_framework.pagination import PageNumberPagination
from rest_framework.generics import ListCreateAPIView, RetrieveUpdateDestroyAPIView


# Paginação
class NewsApiPagination(PageNumberPagination):
    page_size = 2


class NewsApiList(ListCreateAPIView):
    queryset = News.objects.get_published()
    serializer_class = NewsSerializer
    pagination_class = NewsApiPagination


# Ver todas as notícias | publicar uma notícia
# Post desativado
# Ver todas as notícias com paginação do django rest framework
class NewsApiList_(APIView):
    def get(self, request):
        # Pegar todas as notícias publicadas
        news = News.objects.get_published()

        # Serializer + many= +1 notícia
        serializer = NewsSerializer(instance=news, many=True, context={'request': request})
        return Response(serializer.data)

    def post(self, request):
        # Criar uma notícia com API
        serializer = NewsSerializer(data=request.data, context={'request': request})

        # Criar slug personalizado
        date = datetime.now()
        new_date = datetime.strptime(f'{date.day}-{date.month}-{date.year}-{date.microsecond}', '%d-%m-%Y-%f')
        slug = slugify(f"{request.data.get('title')}-{new_date}")

        # Validar campos
        serializer.is_valid(raise_exception=True)

        # Salvar na bd e slug personalizado
        serializer.save(slug=slug)

        return Response(serializer.data, status=status.HTTP_201_CREATED)


# Ver uma notícia | apagar uma notícia | atualizar uma notícia
class NewsApiDetail(APIView):
    def get_news(self, pk):
        # Filtrar uma notícia
        news = News.objects.filter(pk=pk).first()

        return news

    def get(self, request, pk):
        # Pegar uma notícia
        news = self.get_news(pk)

        # Notícia não encontrada = bad request
        if not news:
            return Response(status=status.HTTP_400_BAD_REQUEST)

        # Mostrar uma notícia
        serializer = NewsSerializer(instance=news, many=False, context={'request': request})

        return Response(serializer.data)

    def patch(self, request, pk):
        # Pegar uma notícia
        news = self.get_news(pk)

        # Notícia não encontrada = bad request
        if not news:
            return Response(status=status.HTTP_400_BAD_REQUEST)

        # Atualizar uma notícia
        serializer = NewsSerializer(
            instance=news,
            data=request.data,
            many=False,
            context={'request': request},
            partial=True,

        )

        # Validar campos
        serializer.is_valid(raise_exception=True)

        # Salvar notícia na bd
        serializer.save()

        return Response(serializer.data)

    def delete(self, request, pk):
        # Pegar uma notícia
        news = self.get_news(pk)

        # Notícia não encontrada = bad request
        if not news:
            return Response(status=status.HTTP_400_BAD_REQUEST)

        # Deletar a notícia
        news.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

# Ver uma notícia | apagar uma notícia | atualizar uma notícia
class NewsApiDetail_(RetrieveUpdateDestroyAPIView):
    queryset = News.objects.get_published()
    serializer_class = NewsSerializer
    pagination_class = NewsApiPagination

    def patch(self, request, *args, **kwargs):
        # Pegar pk da notícia
        pk = self.kwargs.get('pk')

        # Pegar uma notícia
        news = self.get_queryset().filter(pk=pk).first()

        # Notícia não encontrada = bad request
        if not news:
            return Response(status=status.HTTP_404_NOT_FOUND)

        # Atualizar uma notícia
        serializer = NewsSerializer(
            instance=news,
            data=request.data,
            many=False,
            context={'request': request},
            partial=True,

        )

        # Validar campos
        serializer.is_valid(raise_exception=True)

        # Salvar notícia na bd
        serializer.save()

        return Response(serializer.data)

from rest_framework import status
from rest_framework.views import APIView
from news.models import News
from tags.models import Tag
from ..serializer import NewsSerializer
from ..serializer import TagSerializer
from rest_framework.response import Response
from rest_framework.pagination import PageNumberPagination
from rest_framework.viewsets import ModelViewSet
from rest_framework.permissions import IsAuthenticatedOrReadOnly
from ..permissions import IsOwner
from django.shortcuts import get_object_or_404


# Paginação
class NewsApiPagination(PageNumberPagination):
    page_size = 10


# Faz tudo, get, post, delete, patch, put...
# Configurar na url
class NewsApiViewSet(ModelViewSet):
    queryset = News.objects.get_published()
    serializer_class = NewsSerializer
    pagination_class = NewsApiPagination
    permission_classes = [IsAuthenticatedOrReadOnly, ]

    # Sobrescrever get_queryset
    # Exemplo da aula de rest, não funciona no meu site
    """def get_queryset(self):
        qs = super().get_queryset()

        category_id = self.request.query_params.get('category_id', '')

        if category_id != '' and category_id.isnumeric():
            qs = qs.filter(category_id=category_id)

        return qs"""

    # Sempre que for criar ele passa aqui
    # Usei para preencher o campo author automaticamente
    def create(self, request, *args, **kwargs):
        # Pegando serializer e editando
        serializer = self.get_serializer(data=request.data)

        # Verificandos se é valido
        serializer.is_valid(raise_exception=True)

        # Salvar e passar o author como o usuário logado
        serializer.save(author=request.user)

        # Obrigatório ter isso
        headers = self.get_success_headers(serializer.data)

        return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)

    def get_object(self):
        # Pegar pk
        pk = self.kwargs.get('pk','')

        # Pegar uma notícia minha
        obj = get_object_or_404(
            self.get_queryset(),
            pk=pk
        )

        # Checar as permissões
        # A minha classe IsOwner
        self.check_object_permissions(self.request, obj)

        return obj

    def get_permissions(self):
        if self.request.method in ['PATCH','DELETE']:
            return [IsOwner(),]

        return super().get_permissions()

    def partial_update(self, request, *args, **kwargs):
        # Pegar uma notícia
        news = self.get_object()

        # Notícia não encontrada = bad request
        if not news:
            return Response(status=status.HTTP_404_NOT_FOUND)

        # Atualizar uma notícia
        serializer = NewsSerializer(
            instance=news,
            data=request.data,
            many=False,
            context={'request': request},
            partial=True,

        )

        # Validar campos
        serializer.is_valid(raise_exception=True)

        # Salvar notícia na bd
        serializer.save()

        return Response(serializer.data)


class TagApiDetail(APIView):
    def get(self, request, pk):
        # Filtrar uma tag
        tag = Tag.objects.filter(pk=pk).first()

        # "Tag" não encontrada = bad request
        if not tag:
            return Response(status=status.HTTP_400_BAD_REQUEST)

        # Pegar uma tag
        serializer = TagSerializer(
            instance=tag,
            many=False,
            context={'request': request}
        )

        return Response(serializer.data)
