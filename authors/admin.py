from django.contrib import admin
from .models import AuthorRegister

# Register your models here.


class AuthorRegisterAdmin(admin.ModelAdmin):
    # Serve pra mostrar a lista de campos no display
    list_display = ('id', 'author', 'is_active')

    # Serve pra realizar buscar com os campos selecionados abaixo
    search_fields = ('id', 'author',)

    # Permite editar algo sem precisar abrir uma nova guia
    list_editable = ('is_active',)

    # Permite mostrar apenas 10 notícias | Se tiver mais cria uma paginação
    list_per_page = 10

    # Permite criar um link, quando eu clicar no link eu abro uma nova guia
    list_display_links = ('id', 'author')

    # Cria um filtro de busca avançado
    list_filter = ('author', 'created_at')


admin.site.register(AuthorRegister, AuthorRegisterAdmin)
