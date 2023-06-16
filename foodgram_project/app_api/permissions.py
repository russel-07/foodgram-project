from rest_framework.permissions import BasePermission


class IsAdminOrReadOnly(BasePermission):
    def has_permission(self, request, view):
        return bool(
            request.method == 'GET' or
            (request.method in ('POST', 'PUT', 'PATCH', 'DELETE') and
            request.user and request.user.is_superuser)
        )
