from rest_framework import permissions


class IsOwnerOrReadOnly(permissions.BasePermission):
    """Класс проверяющий является ли пользователь автором."""

    message = 'User is not superuser'

    def has_permission(self, request, view):
        return request.user.is_authenticated or (
            request.method in permissions.SAFE_METHODS
        )

    def has_object_permission(self, request, view, obj):
        if request.method not in permissions.SAFE_METHODS:
            return (
                request.user.is_admin
                or request.user.is_moderator
                or (obj.author == request.user)
            )
        return request.method in permissions.SAFE_METHODS


class IsAdminOrReadOnly(permissions.BasePermission):
    """Класс проверяющий является ли пользователь автором или админом."""

    message = 'User is not superuser or author'

    def has_permission(self, request, view):
        return request.method in permissions.SAFE_METHODS or (
            request.user.is_authenticated and request.user.is_admin
        )


class IsAdmin(permissions.BasePermission):
    """Класс проверяющий является ли пользователь
    администратором или владельцем."""

    message = 'User is not superuser'

    def has_permission(self, request, view):
        return request.user.is_authenticated and (
            request.user.is_admin or request.user.is_superuser
        )


class IsSelf(permissions.BasePermission):
    def has_permission(self, request, view):
        return request.user.is_authenticated and (
            (request.method in permissions.SAFE_METHODS)
            or (request.method == 'PATCH')
            or (request.method == 'DELETE')
        )
