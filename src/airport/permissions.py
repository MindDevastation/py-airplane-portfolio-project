from rest_framework.permissions import BasePermission, SAFE_METHODS


class CustomAuthUserPermission(BasePermission):
    """
    Custom permission to provide different access levels for users:
    1. Non-authenticated users: Only view (read-only access).
    2. Authenticated users: Can view and create.
    3. Admins/Moderators: Can view, create, update, partially update and delete.
    """

    def has_permission(self, request, view):
        if request.method in SAFE_METHODS:
            return True

        if request.user and request.user.is_authenticated:
            if request.method == "POST":
                return True

            if request.user.is_staff or request.user.is_superuser:
                return True

        return False


class UserPermission(BasePermission):
    """
    1. Unauthorized users can only create a new user.
    2. Authorized users can only view and edit their profile and create new users.
    3. Moderators have full access to all users, but cannot edit superusers.
    4. Superusers have full access with no restrictions.
    """

    def has_permission(self, request, view):
        if request.method == "POST" or (request.user and request.user.is_authenticated):
            return True
        return False

    def has_object_permission(self, request, view, obj):
        if request.user.is_superuser:
            return True

        if request.method in SAFE_METHODS:
            return obj == request.user or request.user.is_staff

        return obj == request.user or (request.user.is_staff and not obj.is_superuser)
