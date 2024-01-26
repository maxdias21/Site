from rest_framework import serializers
from news.models import News
from tags.models import Tag

# Criar campos de forma manual
"""class TagSerializer(serializers.Serializer):
    id = serializers.IntegerField()
    name = serializers.CharField(max_length=100)
    slug = serializers.SlugField()


class NewsSerializer(serializers.Serializer):
    id = serializers.IntegerField()
    author = serializers.PrimaryKeyRelatedField(queryset=User.objects.all())
    title = serializers.CharField(max_length=255)
    description = serializers.CharField(max_length=255)
    content = serializers.CharField(max_length=2000)
    # Pegar as tags da minha notícia
    # Retorna um “id”
    tags = serializers.PrimaryKeyRelatedField(queryset=Tag.objects.all(), many=True)
    # Pegar os dados das tags
    # Retorna todos os dados (id, nome da tag...)
    tags_objects = TagSerializer(many=True, source='tags', read_only=True)

    # Cria um link para ver informações da tag
    tag_links = serializers.HyperlinkedRelatedField(
        many=True,
        source='tags',
        view_name='news:api_news_tag',
        read_only=True,

        # Não precisa quando read_only = True
        # query_set = Tag.objects.all()
    )
"""


# Criar campos usando model

class TagSerializer(serializers.ModelSerializer):
    class Meta:
        model = Tag
        fields = ['id', 'name', 'slug']


class NewsSerializer(serializers.ModelSerializer):
    class Meta:
        model = News
        fields = ['author', 'title', 'description', 'content',
                  'image', 'slug', 'type', 'is_published', 'tags', 'tag_objects', 'tag_links']

    # Pegar os dados das tags
    # Retorna todos os dados (id, nome da tag...)
    tag_objects = TagSerializer(many=True, source='tags', read_only=True)

    # Cria um link para ver informações da tag
    tag_links = serializers.HyperlinkedRelatedField(
        many=True,
        source='tags',
        read_only=True,
        view_name='news:api_news_tag',
    )

