
from rest_framework.permissions import IsAuthenticatedOrReadOnly


class AuthorAdminPermission(IsAuthenticatedOrReadOnly):
    """Права доступа для автора либо алминистратора."""
    def has_object_permission(self, request, view, obj):
        return (request.method == 'GET'
                or (request.user == obj.author)
                or request.user.is_staff)
