"""
Resilio Core Serializers - REST API serialization for R4S models
"""

from rest_framework import serializers
from .models import (
    System, Risk, Actor, Relationship,
    ComponentAssessment, VulnerabilityAssessment
)


class ComponentAssessmentSerializer(serializers.ModelSerializer):
    relevance_score = serializers.ReadOnlyField()

    class Meta:
        model = ComponentAssessment
        fields = [
            'id', 'goods_services', 'production', 'replaceability',
            'rationale', 'relevance_score', 'created_at', 'updated_at'
        ]


class VulnerabilityAssessmentSerializer(serializers.ModelSerializer):
    vulnerability_score = serializers.ReadOnlyField()
    vulnerability_level = serializers.ReadOnlyField()
    risk_name = serializers.CharField(source='risk.name', read_only=True)

    class Meta:
        model = VulnerabilityAssessment
        fields = [
            'id', 'risk', 'risk_name', 'sensitivity', 'exposure', 'capacity',
            'rationale', 'vulnerability_score', 'vulnerability_level',
            'created_at', 'updated_at'
        ]


class ActorListSerializer(serializers.ModelSerializer):
    """Lightweight serializer for actor lists"""
    actor_type_display = serializers.CharField(source='get_actor_type_display', read_only=True)

    class Meta:
        model = Actor
        fields = [
            'id', 'slug', 'name', 'actor_type', 'actor_type_display',
            'position_x', 'position_y'
        ]


class ActorDetailSerializer(serializers.ModelSerializer):
    """Full serializer for actor details"""
    actor_type_display = serializers.CharField(source='get_actor_type_display', read_only=True)
    component_assessment = ComponentAssessmentSerializer(read_only=True)
    vulnerability_assessments = VulnerabilityAssessmentSerializer(many=True, read_only=True)

    class Meta:
        model = Actor
        fields = [
            'id', 'slug', 'name', 'actor_type', 'actor_type_display',
            'aliases', 'function', 'needs', 'worries', 'metadata',
            'position_x', 'position_y',
            'component_assessment', 'vulnerability_assessments',
            'created_at', 'updated_at'
        ]


class RiskSerializer(serializers.ModelSerializer):
    category_display = serializers.CharField(source='get_category_display', read_only=True)
    likelihood_display = serializers.CharField(source='get_likelihood_display', read_only=True)

    class Meta:
        model = Risk
        fields = [
            'id', 'slug', 'name', 'description', 'category', 'category_display',
            'likelihood', 'likelihood_display', 'historical_occurrences',
            'created_at', 'updated_at'
        ]


class RelationshipSerializer(serializers.ModelSerializer):
    from_actor_name = serializers.CharField(source='from_actor.name', read_only=True)
    to_actor_name = serializers.CharField(source='to_actor.name', read_only=True)
    quality_display = serializers.CharField(source='get_quality_display', read_only=True)

    class Meta:
        model = Relationship
        fields = [
            'id', 'from_actor', 'from_actor_name', 'to_actor', 'to_actor_name',
            'relationship_type', 'goods_services', 'quality', 'quality_display',
            'rationale', 'suggested_kpis', 'created_at', 'updated_at'
        ]


class SystemListSerializer(serializers.ModelSerializer):
    """Lightweight serializer for system lists"""
    sector_display = serializers.CharField(source='get_sector_display', read_only=True)
    actor_count = serializers.SerializerMethodField()
    risk_count = serializers.SerializerMethodField()

    class Meta:
        model = System
        fields = [
            'id', 'slug', 'name', 'description', 'region', 'country',
            'sector', 'sector_display', 'subsector', 'assessment_date',
            'version', 'actor_count', 'risk_count', 'updated_at'
        ]

    def get_actor_count(self, obj):
        return obj.actors.count()

    def get_risk_count(self, obj):
        return obj.risks.count()


class SystemDetailSerializer(serializers.ModelSerializer):
    """Full serializer for system details with nested data"""
    sector_display = serializers.CharField(source='get_sector_display', read_only=True)
    actors = ActorDetailSerializer(many=True, read_only=True)
    risks = RiskSerializer(many=True, read_only=True)
    relationships = RelationshipSerializer(many=True, read_only=True)

    class Meta:
        model = System
        fields = [
            'id', 'slug', 'name', 'description', 'region', 'country',
            'sector', 'sector_display', 'subsector', 'assessment_date',
            'version', 'actors', 'risks', 'relationships',
            'created_at', 'updated_at'
        ]


class SystemCreateUpdateSerializer(serializers.ModelSerializer):
    """Serializer for creating/updating systems"""

    class Meta:
        model = System
        fields = [
            'slug', 'name', 'description', 'region', 'country',
            'sector', 'subsector', 'assessment_date', 'version'
        ]


class ActorCreateUpdateSerializer(serializers.ModelSerializer):
    """Serializer for creating/updating actors"""

    class Meta:
        model = Actor
        fields = [
            'system', 'slug', 'name', 'actor_type', 'aliases',
            'function', 'needs', 'worries', 'metadata',
            'position_x', 'position_y'
        ]


class RelationshipCreateUpdateSerializer(serializers.ModelSerializer):
    """Serializer for creating/updating relationships"""

    class Meta:
        model = Relationship
        fields = [
            'system', 'from_actor', 'to_actor', 'relationship_type',
            'goods_services', 'quality', 'rationale', 'suggested_kpis'
        ]


class RiskCreateUpdateSerializer(serializers.ModelSerializer):
    """Serializer for creating/updating risks"""

    class Meta:
        model = Risk
        fields = [
            'system', 'slug', 'name', 'description', 'category',
            'likelihood', 'historical_occurrences'
        ]


class ComponentAssessmentCreateUpdateSerializer(serializers.ModelSerializer):
    """Serializer for creating/updating component assessments"""

    class Meta:
        model = ComponentAssessment
        fields = [
            'actor', 'goods_services', 'production', 'replaceability', 'rationale'
        ]


class VulnerabilityAssessmentCreateUpdateSerializer(serializers.ModelSerializer):
    """Serializer for creating/updating vulnerability assessments"""

    class Meta:
        model = VulnerabilityAssessment
        fields = [
            'actor', 'risk', 'sensitivity', 'exposure', 'capacity', 'rationale'
        ]
