from rest_framework.permissions import BasePermission, SAFE_METHODS


# class Author(BasePermission):

#     def has_object_permission(self, request, view, obj):
#         return request.user and request.user == obj.author


class Follower(BasePermission):

    def has_object_permission(self, request, view, obj):
        return request.user and request.user == obj.user


class ReadOnly(BasePermission):

    def has_object_permission(self, request, view, obj):
        return (
            request.method in SAFE_METHODS
        )


class IsAuthorOrReadOnly(BasePermission):

    def has_permission(self, request, view):
        return (
            request.method in SAFE_METHODS
            or request.user.is_authenticated
        )

    def has_object_permission(self, request, view, obj):
        if request.method in SAFE_METHODS:
            return True
        if request.user and request.user.is_authenticated:
            return (request.user.is_superuser
                    or obj.author == request.user)
        return False
