from django.contrib import admin
from .models import Tag


class TagAdmin(admin.ModelAdmin):
    fields = ('name',)

    # Serve pra mostrar a lista de campos no display
    list_display = ('id', 'name',)

    # Serve pra realizar buscar com os campos selecionados abaixo
    search_fields = ('id', 'name',)

    # Permite mostrar apenas 10 notícias | Se tiver mais cria uma paginação
    list_per_page = 10

    # Permite criar um link, quando eu clicar no link eu abro uma nova guia
    list_display_links = ('id', 'name')


admin.site.register(Tag, TagAdmin)
