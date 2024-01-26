from django.views import View
from django.http import Http404

class NotAuthenticated(View):
    # Dispatch é responsável por retornar um http response (get/post)
    # Usei, pois se o usuário estiver logado, ele retorna para outra página
    def dispatch(self, request, *args, **kwargs):
        if not request.user.is_authenticated:
            raise Http404()

        return super().dispatch(request, *args, **kwargs)


class IsAuthenticated(View):
    # Dispatch é responsável por retornar um http response (get/post)
    # Usei, pois se o usuário estiver logado, ele retorna para outra página
    def dispatch(self, request, *args, **kwargs):
        if request.user.is_authenticated:
            raise Http404()

        return super().dispatch(request, *args, **kwargs)