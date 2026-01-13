"""
Resilio Users Views - Authentication and User Management API
"""

from rest_framework import viewsets, status, generics
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework_simplejwt.views import TokenObtainPairView
from django.db import models

from .models import User, Project, ProjectMembership
from .serializers import (
    CustomTokenObtainPairSerializer,
    UserSerializer, UserCreateSerializer, UserUpdateSerializer,
    UserAdminUpdateSerializer, ChangePasswordSerializer,
    ProjectSerializer, ProjectListSerializer, ProjectCreateUpdateSerializer,
    ProjectMembershipSerializer, AssignManagerSerializer
)
from .permissions import (
    IsSuperadmin, IsSuperadminOrReadOnly, IsR4SManagerOrAbove,
    IsProjectMember, IsProjectManagerOrSuperadmin, IsOwnerOrSuperadmin
)


class CustomTokenObtainPairView(TokenObtainPairView):
    """Custom login endpoint that returns user info with tokens."""
    serializer_class = CustomTokenObtainPairSerializer


class UserViewSet(viewsets.ModelViewSet):
    """
    ViewSet for user management.

    - Superadmins can list, create, update, delete all users
    - Users can view and update their own profile
    """
    queryset = User.objects.all()

    def get_permissions(self):
        if self.action == 'create':
            return [IsSuperadmin()]
        elif self.action in ['list', 'destroy']:
            return [IsSuperadmin()]
        elif self.action in ['retrieve', 'update', 'partial_update']:
            return [IsAuthenticated(), IsOwnerOrSuperadmin()]
        return [IsAuthenticated()]

    def get_serializer_class(self):
        if self.action == 'create':
            return UserCreateSerializer
        elif self.action in ['update', 'partial_update']:
            # Superadmins can update role and is_active
            if self.request.user.role == User.Role.SUPERADMIN:
                return UserAdminUpdateSerializer
            return UserUpdateSerializer
        return UserSerializer

    def get_queryset(self):
        user = self.request.user
        if user.role == User.Role.SUPERADMIN:
            return User.objects.all()
        # Non-superadmins can only see themselves
        return User.objects.filter(id=user.id)

    @action(detail=False, methods=['get', 'put', 'patch'])
    def me(self, request):
        """Get or update the current user's profile."""
        if request.method == 'GET':
            serializer = UserSerializer(request.user)
            return Response(serializer.data)

        serializer = UserUpdateSerializer(
            request.user,
            data=request.data,
            partial=request.method == 'PATCH'
        )
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(UserSerializer(request.user).data)

    @action(detail=False, methods=['post'])
    def change_password(self, request):
        """Change the current user's password."""
        serializer = ChangePasswordSerializer(
            data=request.data,
            context={'request': request}
        )
        serializer.is_valid(raise_exception=True)

        request.user.set_password(serializer.validated_data['new_password'])
        request.user.save()

        return Response({'message': 'Password changed successfully.'})

    @action(detail=False, methods=['get'], permission_classes=[IsSuperadmin])
    def managers(self, request):
        """List all users with R4S Manager role."""
        managers = User.objects.filter(role=User.Role.R4S_MANAGER)
        serializer = UserSerializer(managers, many=True)
        return Response(serializer.data)

    @action(detail=False, methods=['get'], permission_classes=[IsSuperadmin])
    def staff(self, request):
        """List all users with Project Staff role."""
        staff = User.objects.filter(role=User.Role.PROJECT_STAFF)
        serializer = UserSerializer(staff, many=True)
        return Response(serializer.data)


class ProjectViewSet(viewsets.ModelViewSet):
    """
    ViewSet for project management.

    - Superadmins can create, update, delete projects
    - R4S Managers can view projects they're assigned to
    - Project Staff can view projects they're assigned to
    """
    queryset = Project.objects.all()

    def get_permissions(self):
        if self.action in ['create', 'destroy']:
            return [IsSuperadmin()]
        elif self.action in ['update', 'partial_update']:
            return [IsAuthenticated(), IsProjectManagerOrSuperadmin()]
        return [IsAuthenticated()]

    def get_serializer_class(self):
        if self.action == 'list':
            return ProjectListSerializer
        elif self.action in ['create', 'update', 'partial_update']:
            return ProjectCreateUpdateSerializer
        return ProjectSerializer

    def get_queryset(self):
        user = self.request.user
        if user.role == User.Role.SUPERADMIN:
            return Project.objects.all()

        # Non-superadmins can only see projects they're members of
        return Project.objects.filter(memberships__user=user).distinct()

    def perform_create(self, serializer):
        serializer.save(created_by=self.request.user)

    @action(detail=True, methods=['post'], permission_classes=[IsSuperadmin])
    def assign_manager(self, request, pk=None):
        """Assign an R4S Manager to this project."""
        project = self.get_object()
        user_id = request.data.get('user_id')

        try:
            user = User.objects.get(id=user_id)
        except User.DoesNotExist:
            return Response(
                {'error': 'User not found.'},
                status=status.HTTP_404_NOT_FOUND
            )

        if user.role != User.Role.R4S_MANAGER:
            return Response(
                {'error': 'User must have R4S Manager role.'},
                status=status.HTTP_400_BAD_REQUEST
            )

        membership, created = ProjectMembership.objects.update_or_create(
            user=user,
            project=project,
            defaults={
                'role': ProjectMembership.Role.MANAGER,
                'assigned_by': request.user
            }
        )

        serializer = ProjectMembershipSerializer(membership)
        return Response(
            serializer.data,
            status=status.HTTP_201_CREATED if created else status.HTTP_200_OK
        )

    @action(detail=True, methods=['post'], permission_classes=[IsProjectManagerOrSuperadmin])
    def assign_staff(self, request, pk=None):
        """Assign Project Staff to this project."""
        project = self.get_object()
        user_id = request.data.get('user_id')

        try:
            user = User.objects.get(id=user_id)
        except User.DoesNotExist:
            return Response(
                {'error': 'User not found.'},
                status=status.HTTP_404_NOT_FOUND
            )

        membership, created = ProjectMembership.objects.update_or_create(
            user=user,
            project=project,
            defaults={
                'role': ProjectMembership.Role.STAFF,
                'assigned_by': request.user
            }
        )

        serializer = ProjectMembershipSerializer(membership)
        return Response(
            serializer.data,
            status=status.HTTP_201_CREATED if created else status.HTTP_200_OK
        )

    @action(detail=True, methods=['delete'], permission_classes=[IsProjectManagerOrSuperadmin])
    def remove_member(self, request, pk=None):
        """Remove a member from this project."""
        project = self.get_object()
        user_id = request.data.get('user_id')

        try:
            membership = ProjectMembership.objects.get(
                user_id=user_id,
                project=project
            )
            membership.delete()
            return Response(status=status.HTTP_204_NO_CONTENT)
        except ProjectMembership.DoesNotExist:
            return Response(
                {'error': 'Membership not found.'},
                status=status.HTTP_404_NOT_FOUND
            )

    @action(detail=True, methods=['get'])
    def members(self, request, pk=None):
        """List all members of this project."""
        project = self.get_object()
        memberships = project.memberships.all()
        serializer = ProjectMembershipSerializer(memberships, many=True)
        return Response(serializer.data)


class ProjectMembershipViewSet(viewsets.ModelViewSet):
    """ViewSet for managing project memberships directly."""
    queryset = ProjectMembership.objects.all()
    serializer_class = ProjectMembershipSerializer

    def get_permissions(self):
        if self.action in ['create', 'destroy']:
            return [IsSuperadmin()]
        return [IsAuthenticated()]

    def get_queryset(self):
        user = self.request.user
        if user.role == User.Role.SUPERADMIN:
            return ProjectMembership.objects.all()

        # Filter by project membership
        return ProjectMembership.objects.filter(
            models.Q(user=user) |
            models.Q(project__memberships__user=user)
        ).distinct()

    def perform_create(self, serializer):
        serializer.save(assigned_by=self.request.user)
