from rest_framework import permissions


class IsAdminOrReadOnly(permissions.BasePermission):
    """Доступ только для администратора или только для чтения."""

    def has_permission(self, request, view):
        return request.method in permissions.SAFE_METHODS or (
            request.user.is_authenticated and request.user.is_admin
        )


class IsAuthorOrReadOnly(permissions.BasePermission):
    """Доступ только для автора или только для чтения."""

    def has_permission(self, request, view):

        return request.method in permissions.SAFE_METHODS or (
            request.user.is_authenticated)

    def has_object_permission(self, request, view, obj):

        if request.method in permissions.SAFE_METHODS:
            return True
        return obj.author == request.user or request.user.is_staff
