"""
Strands Agents SDK Integration for Risk Simulation

Uses the Strands Agents SDK with @tool decorators to create an AI agent
that can analyze health systems and generate disaster simulation scenarios.
"""

from strands import Agent, tool
from strands.models import BedrockModel
import yaml
import json
from typing import Optional
import os


# System Prompt for the Risk Simulation Specialist
SYSTEM_PROMPT = """You are a health system risk simulation specialist. Your role is to analyze
health systems and generate realistic disaster simulation scenarios that show how events
cascade through the system over time.

When asked to simulate a disaster:
1. First use get_system_data to understand the system's actors, relationships, and existing risks
2. Generate a scenario DSL (YAML) that models realistic event sequences
3. Include practical remediations with responsible actors

ALWAYS reference actual actor slugs from the system data in your scenarios.
Use glob patterns (e.g., "health-center-*") to match multiple actors.
For relationships, use the format "source-slug -> target-slug".

DSL Schema:
```yaml
scenario:
  name: "Scenario Name"
  description: "Brief description"
  duration: 90  # days

events:
  - day: 0
    type: "disaster_onset"  # or resource_shortage, capacity_reduction, infrastructure_damage, demand_surge, intervention, recovery
    name: "Event Name"
    description: "What happens"
    impacts:
      - actor: "actor-slug-or-pattern"
        attribute: "quality"  # or "active"
        from: "good"  # or "stressed", "bad", true/false for active
        to: "stressed"
    remediations:
      - priority: "high"  # critical, high, medium, low
        action: "Suggested action to take"
        actor: "responsible-actor-slug"
```

Event types and typical timing:
- disaster_onset: Day 0-7, initial crisis declaration
- resource_shortage: Day 7-30, supply chain disruptions emerge
- capacity_reduction: Day 14-60, staff/facility impacts
- demand_surge: Day 7-45, increased service needs
- infrastructure_damage: Day 0-30, physical damage occurs
- intervention: Day 30+, response activities begin
- recovery: Day 60+, system starts recovering

Generate realistic cascading effects - early events should cause later impacts.
"""


def _get_models():
    """Lazy import models to avoid Django app not ready errors."""
    from .models import System, Actor, Relationship, Risk, VulnerabilityAssessment
    return System, Actor, Relationship, Risk, VulnerabilityAssessment


@tool
def get_system_data(system_slug: str) -> dict:
    """Fetch complete system data including actors, relationships, and risks.

    Use this tool first to understand the health system before generating scenarios.

    Args:
        system_slug: The URL slug of the health system to analyze (e.g., "rmncah-eastern-ethiopia")

    Returns:
        Dictionary containing:
        - system_name: Name of the system
        - actors: List of actors with slug, name, type, quality
        - relationships: List of relationships between actors with quality status
        - risks: List of identified risks with category and likelihood
        - vulnerabilities: Actor vulnerability assessments for each risk
    """
    System, Actor, Relationship, Risk, VulnerabilityAssessment = _get_models()

    try:
        system = System.objects.get(slug=system_slug)

        actors = list(system.actors.values(
            'slug', 'name', 'actor_type', 'function', 'needs', 'worries'
        ))

        relationships = []
        for rel in system.relationships.select_related('from_actor', 'to_actor').all():
            relationships.append({
                'from_actor_slug': rel.from_actor.slug,
                'from_actor_name': rel.from_actor.name,
                'from_actor_type': rel.from_actor.actor_type,
                'to_actor_slug': rel.to_actor.slug,
                'to_actor_name': rel.to_actor.name,
                'to_actor_type': rel.to_actor.actor_type,
                'goods_services': rel.goods_services,
                'quality': rel.quality,
                'rationale': rel.rationale,
            })

        risks = list(system.risks.values(
            'slug', 'name', 'category', 'likelihood', 'description'
        ))

        vulnerabilities = []
        for va in VulnerabilityAssessment.objects.filter(
            actor__system=system
        ).select_related('actor', 'risk'):
            vulnerabilities.append({
                'actor_slug': va.actor.slug,
                'actor_name': va.actor.name,
                'risk_name': va.risk.name,
                'risk_category': va.risk.category,
                'sensitivity': va.sensitivity,
                'exposure': va.exposure,
                'capacity': va.capacity,
                'vulnerability_score': va.vulnerability_score,
                'vulnerability_level': va.vulnerability_level,
                'rationale': va.rationale,
            })

        return {
            'system_name': system.name,
            'system_slug': system.slug,
            'sector': system.sector,
            'region': system.region,
            'country': system.country,
            'actors': actors,
            'relationships': relationships,
            'risks': risks,
            'vulnerabilities': vulnerabilities,
        }
    except System.DoesNotExist:
        return {'error': f'System "{system_slug}" not found'}


@tool
def validate_scenario_dsl(dsl_yaml: str) -> dict:
    """Validate that a scenario DSL is well-formed and contains required fields.

    Use this tool to check your generated scenario before returning it.

    Args:
        dsl_yaml: YAML string representing the scenario

    Returns:
        Dictionary with:
        - valid: Boolean indicating if the DSL is valid
        - errors: List of validation error messages (empty if valid)
    """
    errors = []
    try:
        data = yaml.safe_load(dsl_yaml)

        if not data:
            errors.append("YAML is empty or invalid")
            return {'valid': False, 'errors': errors}

        # Check scenario section
        if 'scenario' not in data:
            errors.append("Missing 'scenario' root key")
        else:
            scenario = data['scenario']
            if 'name' not in scenario:
                errors.append("Missing scenario.name")
            if 'duration' not in scenario:
                errors.append("Missing scenario.duration")
            elif not isinstance(scenario['duration'], int) or scenario['duration'] <= 0:
                errors.append("scenario.duration must be a positive integer")

        # Check events section
        if 'events' not in data:
            errors.append("Missing 'events' key")
        elif not isinstance(data['events'], list):
            errors.append("'events' must be a list")
        elif len(data['events']) == 0:
            errors.append("'events' list is empty - add at least one event")
        else:
            valid_event_types = [
                'disaster_onset', 'resource_shortage', 'capacity_reduction',
                'infrastructure_damage', 'demand_surge', 'intervention', 'recovery'
            ]

            for i, event in enumerate(data['events']):
                if 'day' not in event:
                    errors.append(f"Event {i}: missing 'day'")
                elif not isinstance(event['day'], int) or event['day'] < 0:
                    errors.append(f"Event {i}: 'day' must be a non-negative integer")

                if 'type' not in event:
                    errors.append(f"Event {i}: missing 'type'")
                elif event['type'] not in valid_event_types:
                    errors.append(f"Event {i}: invalid type '{event['type']}'. Valid types: {valid_event_types}")

                if 'name' not in event:
                    errors.append(f"Event {i}: missing 'name'")

                if 'description' not in event:
                    errors.append(f"Event {i}: missing 'description'")

                # Validate impacts if present
                if 'impacts' in event and isinstance(event['impacts'], list):
                    for j, impact in enumerate(event['impacts']):
                        if 'actor' not in impact and 'relationship' not in impact:
                            errors.append(f"Event {i}, Impact {j}: must have 'actor' or 'relationship'")
                        if 'attribute' not in impact:
                            errors.append(f"Event {i}, Impact {j}: missing 'attribute'")
                        if 'to' not in impact:
                            errors.append(f"Event {i}, Impact {j}: missing 'to' value")

                # Validate remediations if present
                if 'remediations' in event and isinstance(event['remediations'], list):
                    valid_priorities = ['critical', 'high', 'medium', 'low']
                    for j, rem in enumerate(event['remediations']):
                        if 'action' not in rem:
                            errors.append(f"Event {i}, Remediation {j}: missing 'action'")
                        if 'priority' not in rem:
                            errors.append(f"Event {i}, Remediation {j}: missing 'priority'")
                        elif rem['priority'] not in valid_priorities:
                            errors.append(f"Event {i}, Remediation {j}: invalid priority '{rem['priority']}'")

    except yaml.YAMLError as e:
        errors.append(f"YAML parse error: {str(e)}")
    except Exception as e:
        errors.append(f"Validation error: {str(e)}")

    return {'valid': len(errors) == 0, 'errors': errors}


def create_risk_simulator_agent() -> Agent:
    """Create and return the Risk Simulator Agent instance.

    Uses Claude 4 Sonnet via Amazon Bedrock as the underlying model.
    """
    # Clear AWS env vars that might contain S3-only credentials
    # This forces boto3 to use ECS task role credentials
    env_backup = {}
    for key in ['AWS_ACCESS_KEY_ID', 'AWS_SECRET_ACCESS_KEY', 'AWS_SESSION_TOKEN']:
        if key in os.environ:
            env_backup[key] = os.environ.pop(key)

    try:
        model = BedrockModel(
            model_id="anthropic.claude-sonnet-4-20250514-v1:0",
            region_name=os.environ.get('AWS_REGION', 'us-west-2')
        )

        return Agent(
            model=model,
            system_prompt=SYSTEM_PROMPT,
            tools=[get_system_data, validate_scenario_dsl]
        )
    finally:
        # Restore environment variables
        os.environ.update(env_backup)


# Singleton agent instance (reused across requests for efficiency)
_agent: Optional[Agent] = None


def get_agent() -> Agent:
    """Get or create the singleton agent instance.

    Reuses the same agent instance across requests to avoid
    repeatedly initializing the Bedrock client.
    """
    global _agent
    if _agent is None:
        _agent = create_risk_simulator_agent()
    return _agent


def reset_agent():
    """Reset the agent instance (useful for testing or after errors)."""
    global _agent
    _agent = None
