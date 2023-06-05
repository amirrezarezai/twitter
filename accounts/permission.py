from rest_framework.permissions import BasePermission


class IsObjectOwner(BasePermission):
    """
    Permission that only allows owners of an object to access it.
    """

    def has_object_permission(self, request, view, obj):
        return obj.user == request.user or request.method == 'GET'