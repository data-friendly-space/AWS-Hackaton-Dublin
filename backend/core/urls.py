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
from .agents import (
    VisualizationAgentView,
    SimulateAgentView,
    ChatAgentView,
    RiskScenarioListView,
    RiskScenarioDetailView,
)

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

    # Agent endpoints
    path('agents/visualize/<slug:system_slug>/', VisualizationAgentView.as_view(), name='visualization-agent'),
    path('agents/simulate/<slug:system_slug>/', SimulateAgentView.as_view(), name='simulate-agent'),
    path('agents/chat/<slug:system_slug>/', ChatAgentView.as_view(), name='chat-agent'),

    # Risk scenario endpoints
    path('systems/<slug:system_slug>/scenarios/', RiskScenarioListView.as_view(), name='scenario-list'),
    path('systems/<slug:system_slug>/scenarios/<uuid:scenario_id>/', RiskScenarioDetailView.as_view(), name='scenario-detail'),

    path('', include(router.urls)),
]
