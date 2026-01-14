"""
Resilio Core URLs - REST API routing for R4S models
"""

from django.urls import path, include
from rest_framework.routers import DefaultRouter

from .views import (
    SystemViewSet, RiskViewSet, ActorViewSet,
    RelationshipViewSet, ComponentAssessmentViewSet,
    VulnerabilityAssessmentViewSet, health_check, debug_systems
)
from .agents import VisualizationAgentView

router = DefaultRouter()
router.register(r'systems', SystemViewSet, basename='system')
router.register(r'risks', RiskViewSet, basename='risk')
router.register(r'actors', ActorViewSet, basename='actor')
router.register(r'relationships', RelationshipViewSet, basename='relationship')
router.register(r'component-assessments', ComponentAssessmentViewSet, basename='component-assessment')
router.register(r'vulnerability-assessments', VulnerabilityAssessmentViewSet, basename='vulnerability-assessment')

urlpatterns = [
    path('health/', health_check, name='health-check'),
    path('debug/systems/', debug_systems, name='debug-systems'),
    path('agents/visualize/<slug:system_slug>/', VisualizationAgentView.as_view(), name='visualization-agent'),
    path('', include(router.urls)),
]
