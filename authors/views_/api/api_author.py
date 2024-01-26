from rest_framework.viewsets import ReadOnlyModelViewSet
from django.contrib.auth import get_user_model
from .serializer import AuthorSerializer
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.decorators import action


class AuthorViewSet(ReadOnlyModelViewSet):
    serializer_class = AuthorSerializer
    permission_classes = [IsAuthenticated, ]

    def get_queryset(self):
        # Pegar o model de User
        User = get_user_model()

        # Filtrar o meu usuário
        # Único user que eu consigo ver é o meu (quem está logado)
        qs = User.objects.filter(username=self.request.user.username)

        return qs

    # Criar url personalizada
    # O nome da url fica o nome da função (no caso "me")
    @action(
        methods=['GET'],
        detail=False,

    )
    def me(self, request, *args, **kwargs):
        # Pegar a queryset
        obj = self.get_queryset().first()

        # Obter um serializer
        serializer = self.get_serializer(
            instance=obj,
        )

        return Response(serializer.data)
