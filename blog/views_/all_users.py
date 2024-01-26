from django.views.generic import ListView
from authors.models import AuthorRegister


class AllUsers(ListView):
    template_name = 'blog/all_users.html'
    model = AuthorRegister
    context_object_name = 'users'
    paginate_by = 19

    def get_queryset(self):
        qs = super().get_queryset().select_related('author')
        qs = qs.filter(is_active=True)

        return qs
