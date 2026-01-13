"""
Resilio Users Permissions - Role-Based Access Control
"""

from rest_framework import permissions
from .models import User, ProjectMembership


class IsSuperadmin(permissions.BasePermission):
    """Only allow Superadmins."""

    def has_permission(self, request, view):
        return (
            request.user and
            request.user.is_authenticated and
            request.user.role == User.Role.SUPERADMIN
        )


class IsSuperadminOrReadOnly(permissions.BasePermission):
    """Allow read access to all authenticated users, write access only to Superadmins."""

    def has_permission(self, request, view):
        if not request.user or not request.user.is_authenticated:
            return False

        if request.method in permissions.SAFE_METHODS:
            return True

        return request.user.role == User.Role.SUPERADMIN


class IsR4SManagerOrAbove(permissions.BasePermission):
    """Allow R4S Managers and Superadmins."""

    def has_permission(self, request, view):
        return (
            request.user and
            request.user.is_authenticated and
            request.user.role in [User.Role.SUPERADMIN, User.Role.R4S_MANAGER]
        )


class IsProjectMember(permissions.BasePermission):
    """Check if user is a member of the project."""

    def has_object_permission(self, request, view, obj):
        if not request.user or not request.user.is_authenticated:
            return False

        # Superadmins have access to all projects
        if request.user.role == User.Role.SUPERADMIN:
            return True

        # Check if user is a member of this project
        return ProjectMembership.objects.filter(
            user=request.user,
            project=obj
        ).exists()


class IsProjectManagerOrSuperadmin(permissions.BasePermission):
    """Check if user is a manager of the project or a Superadmin."""

    def has_object_permission(self, request, view, obj):
        if not request.user or not request.user.is_authenticated:
            return False

        # Superadmins have access to all projects
        if request.user.role == User.Role.SUPERADMIN:
            return True

        # Check if user is a manager of this project
        return ProjectMembership.objects.filter(
            user=request.user,
            project=obj,
            role=ProjectMembership.Role.MANAGER
        ).exists()


class IsOwnerOrSuperadmin(permissions.BasePermission):
    """Allow users to access their own data, or Superadmins to access any data."""

    def has_object_permission(self, request, view, obj):
        if not request.user or not request.user.is_authenticated:
            return False

        # Superadmins have access to all users
        if request.user.role == User.Role.SUPERADMIN:
            return True

        # Users can only access their own data
        return obj == request.user
