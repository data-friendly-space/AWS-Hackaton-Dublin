"""
Resilio Users Serializers - Authentication and User Management
"""

from rest_framework import serializers
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from django.contrib.auth.password_validation import validate_password
from .models import User, Project, ProjectMembership


class CustomTokenObtainPairSerializer(TokenObtainPairSerializer):
    """Custom JWT token serializer that includes user info."""

    @classmethod
    def get_token(cls, user):
        token = super().get_token(user)
        # Add custom claims
        token['email'] = user.email
        token['role'] = user.role
        token['full_name'] = user.get_full_name()
        return token

    def validate(self, attrs):
        data = super().validate(attrs)
        # Add user info to response
        data['user'] = UserSerializer(self.user).data
        return data


class UserSerializer(serializers.ModelSerializer):
    """Serializer for user profile data."""

    full_name = serializers.CharField(source='get_full_name', read_only=True)
    role_display = serializers.CharField(source='get_role_display', read_only=True)

    class Meta:
        model = User
        fields = [
            'id', 'email', 'first_name', 'last_name', 'full_name',
            'title', 'country', 'department', 'job_title',
            'role', 'role_display', 'is_active',
            'created_at', 'updated_at', 'last_login'
        ]
        read_only_fields = ['id', 'email', 'role', 'is_active', 'created_at', 'updated_at', 'last_login']


class UserCreateSerializer(serializers.ModelSerializer):
    """Serializer for creating new users (Superadmin only)."""

    password = serializers.CharField(write_only=True, required=True, validators=[validate_password])

    class Meta:
        model = User
        fields = [
            'email', 'password',
            'first_name', 'last_name', 'title',
            'country', 'department', 'job_title', 'role'
        ]

    def create(self, validated_data):
        password = validated_data.pop('password')
        user = User(**validated_data)
        user.set_password(password)
        user.save()
        return user


class UserUpdateSerializer(serializers.ModelSerializer):
    """Serializer for updating user profiles."""

    class Meta:
        model = User
        fields = [
            'first_name', 'last_name', 'title',
            'country', 'department', 'job_title'
        ]


class UserAdminUpdateSerializer(serializers.ModelSerializer):
    """Serializer for admin updates (can change role and active status)."""

    class Meta:
        model = User
        fields = [
            'first_name', 'last_name', 'title',
            'country', 'department', 'job_title',
            'role', 'is_active'
        ]


class ChangePasswordSerializer(serializers.Serializer):
    """Serializer for password change."""

    old_password = serializers.CharField(required=True)
    new_password = serializers.CharField(required=True, validators=[validate_password])
    new_password_confirm = serializers.CharField(required=True)

    def validate(self, attrs):
        if attrs['new_password'] != attrs['new_password_confirm']:
            raise serializers.ValidationError({'new_password_confirm': 'Passwords do not match.'})
        return attrs

    def validate_old_password(self, value):
        user = self.context['request'].user
        if not user.check_password(value):
            raise serializers.ValidationError('Current password is incorrect.')
        return value


class MemberUserSerializer(serializers.ModelSerializer):
    """Lightweight user serializer for membership display."""
    full_name = serializers.CharField(source='get_full_name', read_only=True)

    class Meta:
        model = User
        fields = ['id', 'email', 'first_name', 'last_name', 'full_name']


class ProjectMembershipSerializer(serializers.ModelSerializer):
    """Serializer for project memberships."""

    user = MemberUserSerializer(read_only=True)
    user_id = serializers.UUIDField(write_only=True, required=False)
    project_title = serializers.CharField(source='project.title', read_only=True)
    role_display = serializers.CharField(source='get_role_display', read_only=True)
    assigned_by_name = serializers.CharField(source='assigned_by.get_full_name', read_only=True)

    class Meta:
        model = ProjectMembership
        fields = [
            'id', 'user', 'user_id',
            'project', 'project_title',
            'role', 'role_display',
            'assigned_by', 'assigned_by_name', 'assigned_at'
        ]
        read_only_fields = ['id', 'assigned_by', 'assigned_at']


class ProjectSerializer(serializers.ModelSerializer):
    """Serializer for projects."""

    created_by_name = serializers.CharField(source='created_by.get_full_name', read_only=True)
    memberships = ProjectMembershipSerializer(many=True, read_only=True)
    manager_count = serializers.SerializerMethodField()
    staff_count = serializers.SerializerMethodField()

    class Meta:
        model = Project
        fields = [
            'id', 'title', 'description', 'country', 'country_area',
            'created_by', 'created_by_name', 'is_active',
            'memberships', 'manager_count', 'staff_count',
            'created_at', 'updated_at'
        ]
        read_only_fields = ['id', 'created_by', 'created_at', 'updated_at']

    def get_manager_count(self, obj):
        return obj.memberships.filter(role=ProjectMembership.Role.MANAGER).count()

    def get_staff_count(self, obj):
        return obj.memberships.filter(role=ProjectMembership.Role.STAFF).count()


class ProjectListSerializer(serializers.ModelSerializer):
    """Lightweight serializer for project lists."""

    created_by_name = serializers.CharField(source='created_by.get_full_name', read_only=True)
    manager_count = serializers.SerializerMethodField()
    staff_count = serializers.SerializerMethodField()

    class Meta:
        model = Project
        fields = [
            'id', 'title', 'country', 'country_area',
            'created_by_name', 'is_active',
            'manager_count', 'staff_count',
            'created_at', 'updated_at'
        ]

    def get_manager_count(self, obj):
        return obj.memberships.filter(role=ProjectMembership.Role.MANAGER).count()

    def get_staff_count(self, obj):
        return obj.memberships.filter(role=ProjectMembership.Role.STAFF).count()


class ProjectCreateUpdateSerializer(serializers.ModelSerializer):
    """Serializer for creating/updating projects."""

    class Meta:
        model = Project
        fields = ['title', 'description', 'country', 'country_area', 'is_active']


class AssignManagerSerializer(serializers.Serializer):
    """Serializer for assigning a manager to a project."""

    user_id = serializers.UUIDField()
    project_id = serializers.UUIDField()

    def validate_user_id(self, value):
        try:
            user = User.objects.get(id=value)
            if user.role != User.Role.R4S_MANAGER:
                raise serializers.ValidationError('User must have R4S Manager role.')
            return value
        except User.DoesNotExist:
            raise serializers.ValidationError('User not found.')

    def validate_project_id(self, value):
        try:
            Project.objects.get(id=value)
            return value
        except Project.DoesNotExist:
            raise serializers.ValidationError('Project not found.')
