from django.contrib import admin
from .models import (
    System, Risk, Actor, Relationship,
    ComponentAssessment, VulnerabilityAssessment
)


@admin.register(System)
class SystemAdmin(admin.ModelAdmin):
    list_display = ['name', 'sector', 'region', 'country', 'assessment_date', 'updated_at']
    list_filter = ['sector', 'country']
    search_fields = ['name', 'description', 'region']
    prepopulated_fields = {'slug': ('name',)}


@admin.register(Risk)
class RiskAdmin(admin.ModelAdmin):
    list_display = ['name', 'system', 'category', 'likelihood']
    list_filter = ['category', 'likelihood', 'system']
    search_fields = ['name', 'description']
    prepopulated_fields = {'slug': ('name',)}


@admin.register(Actor)
class ActorAdmin(admin.ModelAdmin):
    list_display = ['name', 'system', 'actor_type']
    list_filter = ['actor_type', 'system']
    search_fields = ['name', 'function', 'needs', 'worries']
    prepopulated_fields = {'slug': ('name',)}


@admin.register(Relationship)
class RelationshipAdmin(admin.ModelAdmin):
    list_display = ['from_actor', 'to_actor', 'quality', 'relationship_type']
    list_filter = ['quality', 'relationship_type', 'system']
    search_fields = ['goods_services', 'rationale']


@admin.register(ComponentAssessment)
class ComponentAssessmentAdmin(admin.ModelAdmin):
    list_display = ['actor', 'production', 'replaceability', 'relevance_score']
    list_filter = ['production', 'replaceability']
    search_fields = ['actor__name', 'goods_services']


@admin.register(VulnerabilityAssessment)
class VulnerabilityAssessmentAdmin(admin.ModelAdmin):
    list_display = ['actor', 'risk', 'sensitivity', 'exposure', 'capacity', 'vulnerability_score', 'vulnerability_level']
    list_filter = ['sensitivity', 'exposure', 'capacity']
    search_fields = ['actor__name', 'risk__name']
