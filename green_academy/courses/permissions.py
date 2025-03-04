from rest_framework import permissions

class IsAdminUser(permissions.BasePermission):
    """
    Custom permission to only allow users with the 'admin' role to access the endpoint.
    """
    def has_permission(self, request, view):
        return request.user.role == 'admin'
    

class IsInstructorOrAdmin(permissions.BasePermission):
    def has_permission(self, request, view):
        return request.user.role in ['instructor', 'admin']