from rest_framework.permissions import BasePermission, SAFE_METHODS


class IsSuperuserOrManager(BasePermission):
    """
    Custom permission to allow only superusers and restaurant managers.
    """

    def has_permission(self, request, view):
        return request.user.is_superuser or request.user.user_type == 'manager'


class IsManager(BasePermission):
    """
    Custom permission to allow only restaurant managers to update the menu.
    """

    def has_permission(self, request, view):
        return request.user.user_type == 'manager'


class IsSuperuserOrEmployee(BasePermission):
    """
    Custom permission to allow only superusers and employees to vote.
    """

    def has_permission(self, request, view):
        return request.user.is_superuser or request.user.user_type == 'employee'
