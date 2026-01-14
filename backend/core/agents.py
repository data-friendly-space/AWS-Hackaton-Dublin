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

from .models import System, SystemVisualization


# R4S Visualization Prompt Template - Detailed Framework Style
R4S_PROMPT_TEMPLATE = """You are an R4S (Resilience for Social Systems) visualization specialist.
Generate a Graphviz DOT diagram matching the official R4S framework visual style.

VISUAL STRUCTURE - THREE HORIZONTAL TIERS:

============================================================================
TIER 1 - SUPPORTING FUNCTIONS (Top, cream/yellow background #FEF3C7)
============================================================================
Create category header boxes arranged horizontally:
- LEADERSHIP & GOVERNANCE (icon: building)
- INFORMATION (icon: database)
- SERVICE DELIVERY (icon: medical cross)
- HEALTH FINANCING (icon: dollar)
- MEDICAL SUPPLY/VACCINES/TECHNOLOGY (icon: truck)
- HUMAN RESOURCES (icon: people)

Under each header, list relevant support actors from the data.
Use: style=filled, fillcolor="#FEF3C7", shape=box, fontsize=10

============================================================================
TIER 2 - CORE SERVICE DELIVERY (Middle, salmon/pink background #FEE2E2)
============================================================================
Organize LEFT-TO-RIGHT by Administrative Level columns:

  FEDERAL → REGIONAL → ZONAL → WOREDA → KEBELE → FAMILIES
  (leftmost)                                      (rightmost)

Within each column, show TWO ROWS:
- TOP ROW: Curative/Diagnostic Level (hospitals, clinics)
- BOTTOM ROW: Preventative Level (health posts, outreach, HEWs)

Place service_provider actors in appropriate admin level columns.
Service users (Families, Children, Pregnant Women) go in rightmost column.

Use subgraphs with rank=same to align nodes horizontally.
Use invisible edges to enforce left-to-right ordering.

============================================================================
TIER 3 - REGULATORY & NORMATIVE (Bottom, light green background #D1FAE5)
============================================================================
Create category boxes arranged horizontally:
- LEADERSHIP & GOVERNANCE (policies, standards)
- FINANCING (funding regulations)
- MEDICAL SUPPLY/VACCINES/TECH (quality standards)
- INFORMATION (reporting requirements)
- SERVICE DELIVERY (clinical protocols)
- HUMAN RESOURCES FOR HEALTH (training standards)

Place regulatory actors under appropriate categories.

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
4. Add nodesep=0.5, ranksep=0.8 for spacing
5. Use splines=ortho for right-angle connectors (cleaner look)

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
