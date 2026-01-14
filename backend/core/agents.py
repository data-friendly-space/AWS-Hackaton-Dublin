"""
Bedrock Agent Integration for R4S Visualizations

Provides endpoints for generating R4S-compliant system visualizations
using AWS Bedrock and Claude models.
"""

import boto3
import hashlib
import json
import re
from django.shortcuts import get_object_or_404
from django.conf import settings
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import AllowAny
from rest_framework import status

from .models import System, SystemVisualization, RiskScenario
import yaml


# R4S Visualization Prompt Template - Detailed Framework Style
R4S_PROMPT_TEMPLATE = """You are an R4S (Resilience for Social Systems) visualization specialist.
Generate a Graphviz DOT diagram matching the official R4S framework visual style.

VISUAL STRUCTURE - THREE HORIZONTAL TIERS:

============================================================================
TIER 1 - SUPPORTING FUNCTIONS (Top, cream/yellow background #FEF3C7)
============================================================================
Arrange support actors in 2-3 ROWS within this tier (not all on one line):
- Row 1: Leadership/Governance actors, Information actors
- Row 2: Service Delivery support, Health Financing actors
- Row 3: Medical Supply actors, Human Resources actors

Group by support category but stack VERTICALLY in multiple rows.
Use: style=filled, fillcolor="#FEF3C7", shape=box, fontsize=10
Keep this tier COMPACT - do not spread actors horizontally across entire width.

============================================================================
TIER 2 - CORE SERVICE DELIVERY (Middle, salmon/pink background #FEE2E2)
============================================================================
Organize TOP-TO-BOTTOM by Administrative Level (creating vertical flow):

  FEDERAL (top of tier)
      ↓
  REGIONAL
      ↓
  ZONAL
      ↓
  WOREDA
      ↓
  KEBELE
      ↓
  COMMUNITY/FAMILIES (bottom of tier)

Within each admin level, place nodes side by side:
- Curative services (hospitals, clinics) on left
- Preventative services (health posts, HEWs) on right

Place service_provider actors in appropriate admin level rows.
Service users (Families, Children, Pregnant Women) go at the bottom.

DO NOT use rank=same excessively - let Graphviz flow nodes vertically.
Create separate subgraph clusters for each admin level to enforce vertical stacking.

============================================================================
TIER 3 - REGULATORY & NORMATIVE (Bottom, light green background #D1FAE5)
============================================================================
Arrange regulatory actors in 2-3 ROWS (not all horizontal):
- Group by regulatory function
- Stack vertically within the tier

Place regulatory actors in a compact vertical arrangement.

NODE STYLING:
- Shape: box with rounded corners (shape=box, style="rounded,filled")
- Service Providers: fillcolor="#006e33", fontcolor="white"
- Service Users: fillcolor="#8B5CF6", fontcolor="white"
- Support Actors: fillcolor="#F59E0B", fontcolor="white"
- Regulatory: fillcolor="#DC2626", fontcolor="white"
- Category Headers: fillcolor="#E5E7EB", fontcolor="#1F2937", fontsize=11, fontname="Arial Bold"

EDGE STYLING by relationship quality:
- quality="good": style=solid, color="#006e33", penwidth=2
- quality="stressed": style=dashed, color="#F59E0B", penwidth=2
- quality="bad": style=solid, color="#DC2626", penwidth=2
- quality="absent": style=dotted, color="#9CA3AF", penwidth=1

EDGE TYPES by goods_services content:
- Contains "referral", "patient", "service": color="#006e33" (green) - service flow
- Contains "supply", "drug", "vaccine", "equipment": color="#3B82F6" (blue) - supplies
- Contains "fund", "money", "finance", "payment": color="#F59E0B" (amber) - financing
- Contains "training", "supervision", "report": color="#6B7280" (gray) - oversight

LAYOUT REQUIREMENTS:
1. rankdir=TB (top to bottom for tiers)
2. Use compound=true for edges between clusters
3. Use constraint=false on some edges to allow flexible routing
4. Add nodesep=0.4, ranksep=1.5 for MORE VERTICAL spacing between tiers
5. Use splines=polyline for cleaner connectors
6. Add newrank=true for better vertical tier separation
7. Use ratio=0.7 to make the graph taller than wide
8. Each tier cluster should have its own distinct vertical band
9. Within clusters, arrange nodes in VERTICAL stacks rather than horizontal rows
10. Use rank=same SPARINGLY - only for nodes that truly need horizontal alignment

LEGEND (bottom right):
Create a legend showing:
- Relationship Quality: Good (solid green), Stressed (dashed amber), Bad (solid red), Absent (dotted gray)
- Actor Types: Service Provider, Service User, Support, Regulatory

OUTPUT: Generate ONLY valid Graphviz DOT code. No explanations.

SYSTEM DATA:
{system_data}

Generate the DOT code now:"""


class VisualizationAgentView(APIView):
    """
    API endpoint for generating R4S system visualizations using Bedrock.

    GET /api/agents/visualize/{system_slug}/
        Returns cached visualization if available, otherwise generates new one.

    POST /api/agents/visualize/{system_slug}/
        Force regenerates the visualization (ignores cache).
    """
    permission_classes = [AllowAny]

    def get(self, request, system_slug):
        """Get cached or generate new visualization."""
        try:
            system = get_object_or_404(System, slug=system_slug)
            system_data = self.prepare_system_data(system)
            data_hash = self.compute_hash(system_data)

            # Check cache
            try:
                viz = system.visualization
                if not viz.is_stale(data_hash):
                    return Response({
                        'dot': viz.dot_code,
                        'cached': True,
                        'generated_at': viz.generated_at.isoformat()
                    })
            except SystemVisualization.DoesNotExist:
                pass

            # Generate new visualization
            dot_code = self.invoke_bedrock(system_data)

            # Cache result
            SystemVisualization.objects.update_or_create(
                system=system,
                defaults={'dot_code': dot_code, 'data_hash': data_hash}
            )

            return Response({
                'dot': dot_code,
                'cached': False,
                'generated_at': None
            })
        except Exception as e:
            import traceback
            return Response(
                {'error': str(e), 'traceback': traceback.format_exc()},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )

    def post(self, request, system_slug):
        """Force regenerate visualization (ignore cache)."""
        system = get_object_or_404(System, slug=system_slug)
        system_data = self.prepare_system_data(system)
        data_hash = self.compute_hash(system_data)

        try:
            dot_code = self.invoke_bedrock(system_data)
        except Exception as e:
            return Response(
                {'error': f'Failed to generate visualization: {str(e)}'},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )

        # Update cache
        SystemVisualization.objects.update_or_create(
            system=system,
            defaults={'dot_code': dot_code, 'data_hash': data_hash}
        )

        return Response({
            'dot': dot_code,
            'regenerated': True
        })

    def prepare_system_data(self, system):
        """Prepare system data for the AI prompt with enhanced metadata."""
        actors = system.actors.all()
        relationships = system.relationships.all()

        actors_data = []
        for actor in actors:
            actor_info = {
                'id': str(actor.id),
                'slug': actor.slug,
                'name': actor.name,
                'actor_type': actor.actor_type,
                'function': actor.function,
            }
            # Include metadata fields for R4S visualization
            metadata = actor.metadata or {}
            if 'admin_level' in metadata:
                actor_info['admin_level'] = metadata['admin_level']
            if 'service_type' in metadata:
                actor_info['service_type'] = metadata['service_type']
            if 'support_category' in metadata:
                actor_info['support_category'] = metadata['support_category']
            if 'regulatory_category' in metadata:
                actor_info['regulatory_category'] = metadata['regulatory_category']
            actors_data.append(actor_info)

        relationships_data = []
        for rel in relationships:
            # Get metadata from both actors
            from_metadata = rel.from_actor.metadata or {}
            to_metadata = rel.to_actor.metadata or {}
            relationships_data.append({
                'from_actor': rel.from_actor.name,
                'from_actor_type': rel.from_actor.actor_type,
                'from_admin_level': from_metadata.get('admin_level', 'unknown'),
                'to_actor': rel.to_actor.name,
                'to_actor_type': rel.to_actor.actor_type,
                'to_admin_level': to_metadata.get('admin_level', 'unknown'),
                'goods_services': rel.goods_services,
                'quality': rel.quality,
            })

        return {
            'system_name': system.name,
            'sector': system.sector,
            'country': system.country,
            'region': system.region,
            'actors': actors_data,
            'relationships': relationships_data,
        }

    def compute_hash(self, data):
        """Compute SHA256 hash of system data for cache invalidation."""
        data_str = json.dumps(data, sort_keys=True)
        return hashlib.sha256(data_str.encode()).hexdigest()

    def invoke_bedrock(self, system_data):
        """Invoke Bedrock to generate visualization."""
        import os
        # Temporarily clear AWS env vars to force boto3 to use ECS task role
        # The env vars contain S3 upload credentials that don't have Bedrock access
        env_backup = {}
        for key in ['AWS_ACCESS_KEY_ID', 'AWS_SECRET_ACCESS_KEY', 'AWS_SESSION_TOKEN']:
            if key in os.environ:
                env_backup[key] = os.environ.pop(key)

        try:
            client = boto3.client(
                'bedrock-runtime',
                region_name=getattr(settings, 'AWS_REGION', 'us-west-2')
            )

            prompt = R4S_PROMPT_TEMPLATE.format(
                system_data=json.dumps(system_data, indent=2)
            )

            response = client.invoke_model(
                modelId='anthropic.claude-3-5-sonnet-20241022-v2:0',
                body=json.dumps({
                    'anthropic_version': 'bedrock-2023-05-31',
                    'max_tokens': 8192,
                    'messages': [
                        {
                            'role': 'user',
                            'content': prompt
                        }
                    ]
                })
            )

            result = json.loads(response['body'].read())
            response_text = result['content'][0]['text']

            return self.extract_dot_code(response_text)
        finally:
            # Restore environment variables
            os.environ.update(env_backup)

    def extract_dot_code(self, text):
        """Extract DOT code from model response."""
        # Try to find code block first
        code_block_match = re.search(r'```(?:dot|graphviz)?\s*(digraph[\s\S]*?)```', text)
        if code_block_match:
            return code_block_match.group(1).strip()

        # Try to find digraph directly
        digraph_match = re.search(r'(digraph\s+\w+\s*\{[\s\S]*\})', text)
        if digraph_match:
            return digraph_match.group(1).strip()

        # If no pattern found, assume the whole text is the DOT code
        return text.strip()


class SimulateAgentView(APIView):
    """
    Generate a disaster simulation scenario using Strands Agent.

    POST /api/agents/simulate/{system_slug}/
        Generate a new scenario from a natural language prompt.
        Body: {"prompt": "Simulate a 3-month drought affecting maternal health services"}
        Returns: {"scenario": {...}, "raw_response": "..."}
    """
    permission_classes = [AllowAny]

    def post(self, request, system_slug):
        from .strands_agent import get_agent

        system = get_object_or_404(System, slug=system_slug)
        user_prompt = request.data.get('prompt', '')

        if not user_prompt:
            return Response(
                {'error': 'Missing "prompt" in request body'},
                status=status.HTTP_400_BAD_REQUEST
            )

        try:
            agent = get_agent()

            # Construct the full prompt with context
            full_prompt = f"""For the health system "{system.name}" (slug: {system_slug}), please:
1. First fetch the system data using get_system_data("{system_slug}")
2. Then generate a disaster simulation scenario for: {user_prompt}

Return the scenario as valid YAML following the DSL schema.
After generating, use validate_scenario_dsl to check it's valid.
"""

            result = agent(full_prompt)

            # Extract YAML from response
            response_text = str(result)
            yaml_content = self._extract_yaml(response_text)

            scenario_data = None
            if yaml_content:
                try:
                    scenario_data = yaml.safe_load(yaml_content)
                except yaml.YAMLError:
                    pass

            return Response({
                'scenario': scenario_data,
                'raw_response': response_text,
                'raw_yaml': yaml_content,
            })

        except Exception as e:
            import traceback
            return Response(
                {'error': str(e), 'traceback': traceback.format_exc()},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )

    def _extract_yaml(self, text: str) -> str:
        """Extract YAML content from markdown code blocks."""
        match = re.search(r'```ya?ml\n(.*?)```', text, re.DOTALL)
        return match.group(1).strip() if match else ''


class ChatAgentView(APIView):
    """
    Chat with the Strands Agent for interactive scenario exploration.

    POST /api/agents/chat/{system_slug}/
        Send a message and receive a response.
        Body: {"messages": [{"role": "user", "content": "..."}]}
        Returns: {"message": "...", "scenario": {...} or null}
    """
    permission_classes = [AllowAny]

    def post(self, request, system_slug):
        from .strands_agent import get_agent

        system = get_object_or_404(System, slug=system_slug)
        messages = request.data.get('messages', [])

        if not messages:
            return Response(
                {'error': 'Missing "messages" in request body'},
                status=status.HTTP_400_BAD_REQUEST
            )

        try:
            agent = get_agent()

            # Build conversation context
            context = f"""You are helping explore disaster scenarios for the "{system.name}" health system (slug: {system_slug}).

When the user asks about potential disasters or "what if" scenarios:
1. Use get_system_data("{system_slug}") to understand the system
2. Provide helpful analysis about how the disaster might affect the system
3. If they ask for a simulation, generate a YAML scenario DSL

Previous conversation:
"""
            for msg in messages[:-1]:  # Previous messages as context
                role = msg.get('role', 'user').upper()
                content = msg.get('content', '')
                context += f"{role}: {content}\n\n"

            # Latest user message
            user_message = messages[-1].get('content', '') if messages else ''
            full_prompt = context + f"USER: {user_message}"

            result = agent(full_prompt)
            response_text = str(result)

            # Check if response contains a scenario
            scenario = None
            yaml_content = self._extract_yaml(response_text)
            if yaml_content:
                try:
                    scenario = yaml.safe_load(yaml_content)
                except yaml.YAMLError:
                    pass

            return Response({
                'message': response_text,
                'scenario': scenario
            })

        except Exception as e:
            import traceback
            return Response(
                {'error': str(e), 'traceback': traceback.format_exc()},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )

    def _extract_yaml(self, text: str) -> str:
        """Extract YAML content from markdown code blocks."""
        match = re.search(r'```ya?ml\n(.*?)```', text, re.DOTALL)
        return match.group(1).strip() if match else ''


class RiskScenarioListView(APIView):
    """
    List and create saved risk scenarios for a system.

    GET /api/systems/{system_slug}/scenarios/
        List all saved scenarios for the system.

    POST /api/systems/{system_slug}/scenarios/
        Save a new scenario.
        Body: {"name": "...", "description": "...", "dsl_content": {...}}
    """
    permission_classes = [AllowAny]

    def get(self, request, system_slug):
        system = get_object_or_404(System, slug=system_slug)
        scenarios = system.scenarios.all()

        data = []
        for scenario in scenarios:
            data.append({
                'id': str(scenario.id),
                'name': scenario.name,
                'description': scenario.description,
                'duration': scenario.duration,
                'event_count': scenario.event_count,
                'created_at': scenario.created_at.isoformat(),
                'updated_at': scenario.updated_at.isoformat(),
            })

        return Response(data)

    def post(self, request, system_slug):
        system = get_object_or_404(System, slug=system_slug)

        name = request.data.get('name')
        description = request.data.get('description', '')
        dsl_content = request.data.get('dsl_content')

        if not name:
            return Response(
                {'error': 'Missing "name" in request body'},
                status=status.HTTP_400_BAD_REQUEST
            )

        if not dsl_content:
            return Response(
                {'error': 'Missing "dsl_content" in request body'},
                status=status.HTTP_400_BAD_REQUEST
            )

        # Get user email if authenticated
        created_by = ''
        if hasattr(request, 'user') and request.user.is_authenticated:
            created_by = getattr(request.user, 'email', str(request.user))

        scenario = RiskScenario.objects.create(
            system=system,
            name=name,
            description=description,
            dsl_content=dsl_content,
            created_by=created_by,
        )

        return Response({
            'id': str(scenario.id),
            'name': scenario.name,
            'description': scenario.description,
            'duration': scenario.duration,
            'event_count': scenario.event_count,
            'created_at': scenario.created_at.isoformat(),
        }, status=status.HTTP_201_CREATED)


class RiskScenarioDetailView(APIView):
    """
    Get, update, or delete a specific risk scenario.

    GET /api/systems/{system_slug}/scenarios/{scenario_id}/
        Get full scenario details including DSL content.

    DELETE /api/systems/{system_slug}/scenarios/{scenario_id}/
        Delete the scenario.
    """
    permission_classes = [AllowAny]

    def get(self, request, system_slug, scenario_id):
        system = get_object_or_404(System, slug=system_slug)
        scenario = get_object_or_404(RiskScenario, id=scenario_id, system=system)

        return Response({
            'id': str(scenario.id),
            'name': scenario.name,
            'description': scenario.description,
            'dsl_content': scenario.dsl_content,
            'duration': scenario.duration,
            'event_count': scenario.event_count,
            'created_by': scenario.created_by,
            'created_at': scenario.created_at.isoformat(),
            'updated_at': scenario.updated_at.isoformat(),
        })

    def delete(self, request, system_slug, scenario_id):
        system = get_object_or_404(System, slug=system_slug)
        scenario = get_object_or_404(RiskScenario, id=scenario_id, system=system)
        scenario.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
