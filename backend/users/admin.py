from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from .models import User, Project, ProjectMembership


@admin.register(User)
class UserAdmin(BaseUserAdmin):
    list_display = ['email', 'first_name', 'last_name', 'role', 'is_active', 'last_login']
    list_filter = ['role', 'is_active', 'is_staff', 'country']
    search_fields = ['email', 'first_name', 'last_name']
    ordering = ['email']

    fieldsets = (
        (None, {'fields': ('email', 'password')}),
        ('Personal Info', {'fields': ('first_name', 'last_name', 'title')}),
        ('Organization', {'fields': ('country', 'department', 'job_title')}),
        ('Role & Permissions', {'fields': ('role', 'is_active', 'is_staff', 'is_superuser')}),
        ('Important dates', {'fields': ('last_login', 'date_joined')}),
    )

    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('email', 'first_name', 'last_name', 'password1', 'password2', 'role'),
        }),
    )


class ProjectMembershipInline(admin.TabularInline):
    model = ProjectMembership
    extra = 1
    autocomplete_fields = ['user']
    readonly_fields = ['assigned_by', 'assigned_at']


@admin.register(Project)
class ProjectAdmin(admin.ModelAdmin):
    list_display = ['title', 'country', 'country_area', 'is_active', 'created_by', 'created_at']
    list_filter = ['is_active', 'country']
    search_fields = ['title', 'description', 'country', 'country_area']
    readonly_fields = ['created_by', 'created_at', 'updated_at']
    inlines = [ProjectMembershipInline]

    def save_model(self, request, obj, form, change):
        if not change:  # Only set created_by on creation
            obj.created_by = request.user
        super().save_model(request, obj, form, change)


@admin.register(ProjectMembership)
class ProjectMembershipAdmin(admin.ModelAdmin):
    list_display = ['user', 'project', 'role', 'assigned_by', 'assigned_at']
    list_filter = ['role', 'project']
    search_fields = ['user__email', 'user__first_name', 'project__title']
    autocomplete_fields = ['user', 'project', 'assigned_by']
    readonly_fields = ['assigned_at']
