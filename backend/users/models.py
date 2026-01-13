"""
Resilio Users - Custom User model with RBAC
"""

from django.contrib.auth.models import AbstractUser, BaseUserManager
from django.db import models
import uuid


class UserManager(BaseUserManager):
    """Custom user manager for email-based authentication."""

    def create_user(self, email, password=None, **extra_fields):
        if not email:
            raise ValueError('The Email field must be set')
        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
        extra_fields.setdefault('role', User.Role.SUPERADMIN)

        if extra_fields.get('is_staff') is not True:
            raise ValueError('Superuser must have is_staff=True.')
        if extra_fields.get('is_superuser') is not True:
            raise ValueError('Superuser must have is_superuser=True.')

        return self.create_user(email, password, **extra_fields)


class User(AbstractUser):
    """
    Custom User model with profile fields and role-based access control.
    """

    class Role(models.TextChoices):
        SUPERADMIN = 'superadmin', 'Superadmin'
        R4S_MANAGER = 'r4s_manager', 'R4S Manager'
        PROJECT_STAFF = 'project_staff', 'Project Staff'

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)

    # Use email as the username field
    username = None
    email = models.EmailField('email address', unique=True)

    # Profile fields
    first_name = models.CharField(max_length=150)
    last_name = models.CharField(max_length=150)
    title = models.CharField(max_length=50, blank=True, help_text='e.g., Mr, Ms, Dr')
    country = models.CharField(max_length=100, blank=True)
    department = models.CharField(max_length=200, blank=True)
    job_title = models.CharField(max_length=200, blank=True)

    # Role
    role = models.CharField(
        max_length=20,
        choices=Role.choices,
        default=Role.PROJECT_STAFF
    )

    # Timestamps
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    objects = UserManager()

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['first_name', 'last_name']

    class Meta:
        ordering = ['email']
        verbose_name = 'User'
        verbose_name_plural = 'Users'

    def __str__(self):
        return f"{self.get_full_name()} ({self.email})"

    def get_full_name(self):
        full_name = f"{self.first_name} {self.last_name}".strip()
        return full_name or self.email

    @property
    def is_superadmin(self):
        return self.role == self.Role.SUPERADMIN

    @property
    def is_r4s_manager(self):
        return self.role == self.Role.R4S_MANAGER

    @property
    def is_project_staff(self):
        return self.role == self.Role.PROJECT_STAFF


class Project(models.Model):
    """
    Project for organizing R4S system mappings.
    Projects have assigned managers and staff.
    """

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    title = models.CharField(max_length=200)
    description = models.TextField(blank=True)
    country = models.CharField(max_length=100)
    country_area = models.CharField(max_length=200, blank=True, help_text='Region, state, or district')

    # Project owner (Superadmin who created it)
    created_by = models.ForeignKey(
        User,
        on_delete=models.SET_NULL,
        null=True,
        related_name='created_projects'
    )

    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-created_at']
        verbose_name = 'Project'
        verbose_name_plural = 'Projects'

    def __str__(self):
        return f"{self.title} ({self.country})"

    @property
    def managers(self):
        """Get all R4S Managers assigned to this project."""
        return User.objects.filter(
            project_memberships__project=self,
            project_memberships__role=ProjectMembership.Role.MANAGER
        )

    @property
    def staff(self):
        """Get all Project Staff assigned to this project."""
        return User.objects.filter(
            project_memberships__project=self,
            project_memberships__role=ProjectMembership.Role.STAFF
        )


class ProjectMembership(models.Model):
    """
    Links users to projects with specific roles.
    """

    class Role(models.TextChoices):
        MANAGER = 'manager', 'R4S Manager'
        STAFF = 'staff', 'Project Staff'

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='project_memberships'
    )
    project = models.ForeignKey(
        Project,
        on_delete=models.CASCADE,
        related_name='memberships'
    )
    role = models.CharField(
        max_length=20,
        choices=Role.choices,
        default=Role.STAFF
    )

    assigned_by = models.ForeignKey(
        User,
        on_delete=models.SET_NULL,
        null=True,
        related_name='assigned_memberships'
    )
    assigned_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ['user', 'project']
        ordering = ['project', 'role', 'user__email']
        verbose_name = 'Project Membership'
        verbose_name_plural = 'Project Memberships'

    def __str__(self):
        return f"{self.user.email} - {self.project.title} ({self.get_role_display()})"
