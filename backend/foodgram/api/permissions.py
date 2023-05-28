from rest_framework import permissions


class IsAdminOrAuthorOrReadOnly(permissions.BasePermission):
    """Класс, проверяющий является ли пользователь
    админом или автором."""

    def has_permission(self, request, view):
        return request.user.is_authenticated or (
            request.method in permissions.SAFE_METHODS
        )

    def has_object_permission(self, request, view, obj):
        if request.method not in permissions.SAFE_METHODS:
            return (
                request.user.is_staff
                or (obj.author == request.user)
            )
        return request.method in permissions.SAFE_METHODS


class IsAdminOrReadOnly(permissions.BasePermission):
    """Класс, проверяющий является ли пользователь
    админом."""

    def has_permission(self, request, view):
        return request.user.is_authenticated or (
            request.method in permissions.SAFE_METHODS
        )

    def has_object_permission(self, request, view, obj):
        if request.method not in permissions.SAFE_METHODS:
            return request.user.is_staff
        return request.method in permissions.SAFE_METHODS
