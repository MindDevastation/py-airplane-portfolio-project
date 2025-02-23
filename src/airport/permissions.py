from rest_framework.permissions import BasePermission

class CustomAuthUserPermission(BasePermission):
    """
    Custom permission to provide different access levels for users:
    1. Non-authenticated users: Only view (read-only access).
    2. Authenticated users: Can view and create.
    3. Admins/Moderators: Can view, create, update, partially update and delete.
    """

    def has_permission(self, request, view):
        if request.method in ['GET', 'HEAD', 'OPTIONS']:
            return True

        if request.user and request.user.is_authenticated:
            if request.method == 'POST':
                return True

            if request.user.is_staff or request.user.is_superuser:
                return True

        return False
