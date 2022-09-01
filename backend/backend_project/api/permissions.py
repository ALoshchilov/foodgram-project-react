from rest_framework.permissions import BasePermission, SAFE_METHODS


class Author(BasePermission):

    def has_object_permission(self, request, view, obj):
        return request.user == obj.author


class Follower(BasePermission):

    def has_object_permission(self, request, view, obj):
        return request.user == obj.user


class ReadOnly(BasePermission):

    def has_object_permission(self, request, view, obj):
        return (
            request.method in SAFE_METHODS
        )
