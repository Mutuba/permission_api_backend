from rest_framework import permissions


class UserHasPermission(permissions.BasePermission):
    def __init__(self, permission):
        self.permission = permission

    def has_permission(self, request, view):
        permissions = request.user.permissions
        if self.permission in permissions:
            return True
        return False
