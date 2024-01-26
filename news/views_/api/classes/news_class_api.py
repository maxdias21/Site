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
