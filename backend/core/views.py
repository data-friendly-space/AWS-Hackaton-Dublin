"""
Resilio Core Views - REST API ViewSets for R4S models
"""

from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response
from django.db import models as db_models

from .models import (
    System, Risk, Actor, Relationship,
    ComponentAssessment, VulnerabilityAssessment
)
from .serializers import (
    SystemListSerializer, SystemDetailSerializer, SystemCreateUpdateSerializer,
    RiskSerializer, RiskCreateUpdateSerializer,
    ActorListSerializer, ActorDetailSerializer, ActorCreateUpdateSerializer,
    RelationshipSerializer, RelationshipCreateUpdateSerializer,
    ComponentAssessmentSerializer, ComponentAssessmentCreateUpdateSerializer,
    VulnerabilityAssessmentSerializer, VulnerabilityAssessmentCreateUpdateSerializer,
)


class SystemViewSet(viewsets.ModelViewSet):
    """
    ViewSet for System CRUD operations.

    list: Returns lightweight system list with counts
    retrieve: Returns full system with nested actors, risks, relationships
    """
    queryset = System.objects.all()
    lookup_field = 'slug'

    def get_serializer_class(self):
        if self.action == 'list':
            return SystemListSerializer
        elif self.action in ['create', 'update', 'partial_update']:
            return SystemCreateUpdateSerializer
        return SystemDetailSerializer

    def get_queryset(self):
        queryset = System.objects.all()

        # Filter by sector
        sector = self.request.query_params.get('sector')
        if sector:
            queryset = queryset.filter(sector=sector)

        # Filter by country
        country = self.request.query_params.get('country')
        if country:
            queryset = queryset.filter(country__icontains=country)

        return queryset

    @action(detail=True, methods=['get'])
    def export(self, request, slug=None):
        """Export system in DSL format"""
        system = self.get_object()
        dsl_output = self._generate_dsl(system)
        return Response({'dsl': dsl_output})

    def _generate_dsl(self, system):
        """Generate DSL text from system data"""
        lines = []

        # System definition
        lines.append(f'system "{system.name}" {{')
        lines.append(f'    slug: "{system.slug}"')
        lines.append(f'    sector: {system.sector}')
        if system.region:
            lines.append(f'    region: "{system.region}"')
        if system.country:
            lines.append(f'    country: "{system.country}"')
        lines.append('}')
        lines.append('')

        # Risks
        for risk in system.risks.all():
            lines.append(f'risk "{risk.name}" {{')
            lines.append(f'    slug: "{risk.slug}"')
            lines.append(f'    category: {risk.category}')
            lines.append(f'    likelihood: {risk.likelihood}')
            if risk.description:
                lines.append(f'    description: "{risk.description}"')
            lines.append('}')
            lines.append('')

        # Actors
        for actor in system.actors.all():
            lines.append(f'actor "{actor.name}" {{')
            lines.append(f'    slug: "{actor.slug}"')
            lines.append(f'    type: {actor.actor_type}')
            lines.append(f'    function: "{actor.function}"')
            lines.append(f'    needs: "{actor.needs}"')
            lines.append(f'    worries: "{actor.worries}"')
            lines.append('}')
            lines.append('')

        # Relationships
        for rel in system.relationships.all():
            arrow = '->' if rel.relationship_type == 'output' else '<-'
            lines.append(f'relationship "{rel.from_actor.slug}" {arrow} "{rel.to_actor.slug}" {{')
            lines.append(f'    goods_services: "{rel.goods_services}"')
            lines.append(f'    quality: {rel.quality}')
            lines.append(f'    rationale: "{rel.rationale}"')
            lines.append('}')
            lines.append('')

        # Component assessments
        for actor in system.actors.all():
            if hasattr(actor, 'component_assessment'):
                ca = actor.component_assessment
                lines.append(f'component "{actor.slug}" {{')
                lines.append(f'    goods_services: "{ca.goods_services}"')
                lines.append(f'    production: {ca.production}')
                lines.append(f'    replaceability: {ca.replaceability}')
                lines.append(f'    rationale: "{ca.rationale}"')
                lines.append('}')
                lines.append('')

        # Vulnerability assessments
        for va in VulnerabilityAssessment.objects.filter(actor__system=system):
            lines.append(f'vulnerability "{va.actor.slug}" @ "{va.risk.slug}" {{')
            lines.append(f'    sensitivity: {va.sensitivity}')
            lines.append(f'    exposure: {va.exposure}')
            lines.append(f'    capacity: {va.capacity}')
            lines.append(f'    rationale: "{va.rationale}"')
            lines.append('}')
            lines.append('')

        return '\n'.join(lines)


class RiskViewSet(viewsets.ModelViewSet):
    """ViewSet for Risk CRUD operations"""
    queryset = Risk.objects.all()

    def get_serializer_class(self):
        if self.action in ['create', 'update', 'partial_update']:
            return RiskCreateUpdateSerializer
        return RiskSerializer

    def get_queryset(self):
        queryset = Risk.objects.all()

        # Filter by system
        system_slug = self.request.query_params.get('system')
        if system_slug:
            queryset = queryset.filter(system__slug=system_slug)

        # Filter by category
        category = self.request.query_params.get('category')
        if category:
            queryset = queryset.filter(category=category)

        return queryset


class ActorViewSet(viewsets.ModelViewSet):
    """ViewSet for Actor CRUD operations"""
    queryset = Actor.objects.all()

    def get_serializer_class(self):
        if self.action == 'list':
            return ActorListSerializer
        elif self.action in ['create', 'update', 'partial_update']:
            return ActorCreateUpdateSerializer
        return ActorDetailSerializer

    def get_queryset(self):
        queryset = Actor.objects.all()

        # Filter by system
        system_slug = self.request.query_params.get('system')
        if system_slug:
            queryset = queryset.filter(system__slug=system_slug)

        # Filter by actor type
        actor_type = self.request.query_params.get('type')
        if actor_type:
            queryset = queryset.filter(actor_type=actor_type)

        return queryset

    @action(detail=True, methods=['patch'])
    def position(self, request, pk=None):
        """Update actor position for visualization"""
        actor = self.get_object()
        actor.position_x = request.data.get('x', actor.position_x)
        actor.position_y = request.data.get('y', actor.position_y)
        actor.save()
        return Response({
            'id': actor.id,
            'position_x': actor.position_x,
            'position_y': actor.position_y
        })


class RelationshipViewSet(viewsets.ModelViewSet):
    """ViewSet for Relationship CRUD operations"""
    queryset = Relationship.objects.all()

    def get_serializer_class(self):
        if self.action in ['create', 'update', 'partial_update']:
            return RelationshipCreateUpdateSerializer
        return RelationshipSerializer

    def get_queryset(self):
        queryset = Relationship.objects.all()

        # Filter by system
        system_slug = self.request.query_params.get('system')
        if system_slug:
            queryset = queryset.filter(system__slug=system_slug)

        # Filter by quality
        quality = self.request.query_params.get('quality')
        if quality:
            queryset = queryset.filter(quality=quality)

        # Filter by actor (either from or to)
        actor_id = self.request.query_params.get('actor')
        if actor_id:
            queryset = queryset.filter(
                db_models.Q(from_actor_id=actor_id) | db_models.Q(to_actor_id=actor_id)
            )

        return queryset


class ComponentAssessmentViewSet(viewsets.ModelViewSet):
    """ViewSet for ComponentAssessment CRUD operations"""
    queryset = ComponentAssessment.objects.all()

    def get_serializer_class(self):
        if self.action in ['create', 'update', 'partial_update']:
            return ComponentAssessmentCreateUpdateSerializer
        return ComponentAssessmentSerializer

    def get_queryset(self):
        queryset = ComponentAssessment.objects.all()

        # Filter by system
        system_slug = self.request.query_params.get('system')
        if system_slug:
            queryset = queryset.filter(actor__system__slug=system_slug)

        return queryset


class VulnerabilityAssessmentViewSet(viewsets.ModelViewSet):
    """ViewSet for VulnerabilityAssessment CRUD operations"""
    queryset = VulnerabilityAssessment.objects.all()

    def get_serializer_class(self):
        if self.action in ['create', 'update', 'partial_update']:
            return VulnerabilityAssessmentCreateUpdateSerializer
        return VulnerabilityAssessmentSerializer

    def get_queryset(self):
        queryset = VulnerabilityAssessment.objects.all()

        # Filter by system
        system_slug = self.request.query_params.get('system')
        if system_slug:
            queryset = queryset.filter(actor__system__slug=system_slug)

        # Filter by risk
        risk_id = self.request.query_params.get('risk')
        if risk_id:
            queryset = queryset.filter(risk_id=risk_id)

        return queryset
