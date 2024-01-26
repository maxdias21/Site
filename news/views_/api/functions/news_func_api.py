from rest_framework.decorators import api_view
from rest_framework.response import Response
from news.models import News
from news.views_.api.serializer import NewsSerializer, TagSerializer
from rest_framework import status
from tags.models import Tag
from datetime import datetime
from django.utils.text import slugify
from rest_framework.pagination import PageNumberPagination


# Ver todas as notícias e criar uma notícia
@api_view(http_method_names=['GET', 'POST'])
def api_all_news(request):
    if request.method == 'GET':
        # Pegar todas as notícias publicadas
        news = News.objects.get_published()

        # Serializer + many= +1 notícia
        serializer = NewsSerializer(instance=news, many=True, context={'request': request})
        return Response(serializer.data)

    elif request.method == 'POST':
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


# Ver uma notícia + atualizar uma notícia + deletar uma notícia
@api_view(http_method_names=['GET', 'PATCH', 'DELETE'])
def api_get_one_news(request, pk):
    # Filtrar uma notícia
    news = News.objects.filter(pk=pk).first()

    # Notícia não encontrada = bad request
    if not news:
        return Response(status=status.HTTP_400_BAD_REQUEST)

    if request.method == 'GET':
        # Mostrar uma notícia
        serializer = NewsSerializer(instance=news, many=False, context={'request': request})

        return Response(serializer.data)

    if request.method == 'PATCH':
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

    if request.method == 'DELETE':
        # Deletar a notícia
        news.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


@api_view()
def api_tag_api_detail(request, pk):
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
