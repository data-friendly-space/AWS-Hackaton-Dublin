"""
Resilio Core Models - R4S Social System Mapping

Models for representing:
- Systems and their metadata
- Risk scenarios
- Actors and their assessments
- Relationships between actors
- Component assessments
- Vulnerability assessments
"""

from django.db import models
from django.core.validators import MinValueValidator, MaxValueValidator
import uuid


class System(models.Model):
    """
    Represents a social system being mapped (e.g., RMNCAH Health System).
    """
    SECTOR_CHOICES = [
        ('health', 'Health'),
        ('education', 'Education'),
        ('market', 'Market'),
        ('water', 'Water/WASH'),
        ('protection', 'Protection'),
        ('nutrition', 'Nutrition'),
        ('shelter', 'Shelter'),
        ('livelihoods', 'Livelihoods'),
    ]

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    slug = models.SlugField(max_length=100, unique=True)
    name = models.CharField(max_length=200)
    description = models.TextField(blank=True)

    region = models.CharField(max_length=200, blank=True)
    country = models.CharField(max_length=100, blank=True)
    sector = models.CharField(max_length=50, choices=SECTOR_CHOICES)
    subsector = models.CharField(max_length=100, blank=True)

    assessment_date = models.DateField(null=True, blank=True)
    version = models.CharField(max_length=20, default='1.0')

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-updated_at']
        verbose_name_plural = 'Systems'

    def __str__(self):
        return self.name


class Risk(models.Model):
    """
    Risk scenarios that affect system actors.
    """
    CATEGORY_CHOICES = [
        ('climate', 'Climate'),
        ('health', 'Health'),
        ('economic', 'Economic'),
        ('conflict', 'Conflict'),
        ('natural', 'Natural Disaster'),
        ('political', 'Political'),
    ]

    LIKELIHOOD_CHOICES = [
        ('rare', 'Rare (<10%)'),
        ('unlikely', 'Unlikely (10-30%)'),
        ('possible', 'Possible (30-60%)'),
        ('likely', 'Likely (60-90%)'),
        ('almost_certain', 'Almost Certain (>90%)'),
    ]

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    system = models.ForeignKey(System, on_delete=models.CASCADE, related_name='risks')
    slug = models.SlugField(max_length=100)

    name = models.CharField(max_length=200)
    description = models.TextField(blank=True)
    category = models.CharField(max_length=50, choices=CATEGORY_CHOICES)
    likelihood = models.CharField(max_length=50, choices=LIKELIHOOD_CHOICES, default='possible')
    historical_occurrences = models.TextField(blank=True, help_text='Years when this risk occurred')

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['name']
        unique_together = ['system', 'slug']

    def __str__(self):
        return f"{self.name} ({self.system.name})"


class Actor(models.Model):
    """
    System actors - entities that participate in the social system.
    """
    TYPE_CHOICES = [
        ('service_user', 'Service User'),
        ('service_provider', 'Service Provider'),
        ('support', 'Support'),
        ('regulatory', 'Regulatory'),
    ]

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    system = models.ForeignKey(System, on_delete=models.CASCADE, related_name='actors')
    slug = models.SlugField(max_length=100)

    name = models.CharField(max_length=200)
    actor_type = models.CharField(max_length=50, choices=TYPE_CHOICES)
    aliases = models.JSONField(default=list, blank=True, help_text='Alternative names for this actor')

    function = models.TextField(help_text='Role and significance within the system')
    needs = models.TextField(help_text='Essential services or conditions the actor expects')
    worries = models.TextField(help_text='Main risks, challenges, or adverse conditions')

    metadata = models.JSONField(default=dict, blank=True)

    # Position for visualization (optional)
    position_x = models.FloatField(null=True, blank=True)
    position_y = models.FloatField(null=True, blank=True)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['name']
        unique_together = ['system', 'slug']

    def __str__(self):
        return f"{self.name} ({self.get_actor_type_display()})"


class Relationship(models.Model):
    """
    Relationships between actors - flow of goods, services, and resources.
    """
    TYPE_CHOICES = [
        ('input', 'Input'),
        ('output', 'Output'),
    ]

    QUALITY_CHOICES = [
        ('good', 'Good'),
        ('stressed', 'Stressed'),
        ('bad', 'Bad'),
        ('absent', 'Absent'),
    ]

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    system = models.ForeignKey(System, on_delete=models.CASCADE, related_name='relationships')

    from_actor = models.ForeignKey(
        Actor,
        on_delete=models.CASCADE,
        related_name='outgoing_relationships'
    )
    to_actor = models.ForeignKey(
        Actor,
        on_delete=models.CASCADE,
        related_name='incoming_relationships'
    )

    relationship_type = models.CharField(max_length=50, choices=TYPE_CHOICES, default='output')
    goods_services = models.TextField(help_text='Specific goods, services, and/or resources exchanged')

    quality = models.CharField(max_length=50, choices=QUALITY_CHOICES)
    rationale = models.TextField(help_text='Reason for the quality assessment')

    suggested_kpis = models.JSONField(
        default=list,
        blank=True,
        help_text='Suggested key performance indicators'
    )

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['from_actor__name', 'to_actor__name']

    def __str__(self):
        return f"{self.from_actor.name} -> {self.to_actor.name} ({self.quality})"


class ComponentAssessment(models.Model):
    """
    Component assessment - evaluates actor importance through production and replaceability.
    """
    SCALE_CHOICES = [(i, str(i)) for i in range(1, 6)]

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    actor = models.OneToOneField(
        Actor,
        on_delete=models.CASCADE,
        related_name='component_assessment'
    )

    goods_services = models.TextField(help_text='Goods/services/resources provided by the actor')

    production = models.IntegerField(
        validators=[MinValueValidator(1), MaxValueValidator(5)],
        help_text='Level of production/throughput (1-5)'
    )
    replaceability = models.IntegerField(
        validators=[MinValueValidator(1), MaxValueValidator(5)],
        help_text='Level of replaceability (1-5, where 5 = not replaceable)'
    )

    rationale = models.TextField(help_text='Reason for the assessment scores')

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = 'Component Assessment'
        verbose_name_plural = 'Component Assessments'

    @property
    def relevance_score(self):
        """Calculate relevance score: production * replaceability"""
        return self.production * self.replaceability

    def __str__(self):
        return f"{self.actor.name} - Relevance: {self.relevance_score}"


class VulnerabilityAssessment(models.Model):
    """
    Vulnerability assessment - evaluates how risk scenarios affect actors.
    """
    SCALE_CHOICES = [(i, str(i)) for i in range(1, 6)]

    LEVEL_CHOICES = [
        ('minimal', 'Minimal'),
        ('low', 'Low'),
        ('medium', 'Medium'),
        ('high', 'High'),
    ]

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    actor = models.ForeignKey(
        Actor,
        on_delete=models.CASCADE,
        related_name='vulnerability_assessments'
    )
    risk = models.ForeignKey(
        Risk,
        on_delete=models.CASCADE,
        related_name='vulnerability_assessments'
    )

    sensitivity = models.IntegerField(
        validators=[MinValueValidator(1), MaxValueValidator(5)],
        help_text='How badly the actor is affected (1-5)'
    )
    exposure = models.IntegerField(
        validators=[MinValueValidator(1), MaxValueValidator(5)],
        help_text='How likely the actor is exposed (1-5)'
    )
    capacity = models.IntegerField(
        validators=[MinValueValidator(1), MaxValueValidator(5)],
        help_text='Ability to resist/adapt (1-5)'
    )

    rationale = models.TextField(help_text='Reason for the assessment scores')

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = 'Vulnerability Assessment'
        verbose_name_plural = 'Vulnerability Assessments'
        unique_together = ['actor', 'risk']

    @property
    def vulnerability_score(self):
        """Calculate vulnerability score: (sensitivity + exposure) / capacity"""
        if self.capacity == 0:
            return 25.0  # Max score if no capacity
        return round((self.sensitivity + self.exposure) / self.capacity, 1)

    @property
    def vulnerability_level(self):
        """Determine vulnerability level from score"""
        score = self.vulnerability_score
        if score <= 1.0:
            return 'minimal'
        elif score <= 8.33:
            return 'low'
        elif score <= 16.66:
            return 'medium'
        else:
            return 'high'

    def __str__(self):
        return f"{self.actor.name} @ {self.risk.name}: {self.vulnerability_score} ({self.vulnerability_level})"


class SystemVisualization(models.Model):
    """
    Cached R4S visualization for a system.
    Stores generated Graphviz DOT code from Bedrock AI analysis.
    """
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    system = models.OneToOneField(
        System,
        on_delete=models.CASCADE,
        related_name='visualization'
    )
    dot_code = models.TextField(help_text='Generated Graphviz DOT code')
    data_hash = models.CharField(
        max_length=64,
        help_text='SHA256 hash of system data to detect changes'
    )
    generated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = 'System Visualization'
        verbose_name_plural = 'System Visualizations'

    def is_stale(self, current_hash: str) -> bool:
        """Check if cached visualization is outdated."""
        return self.data_hash != current_hash

    def __str__(self):
        return f"Visualization for {self.system.name}"


class RiskScenario(models.Model):
    """
    Saved disaster simulation scenario for a system.
    Stores DSL content generated by the Strands Agent.
    """
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    system = models.ForeignKey(
        System,
        on_delete=models.CASCADE,
        related_name='scenarios'
    )
    name = models.CharField(max_length=255)
    description = models.TextField(blank=True)
    dsl_content = models.JSONField(
        help_text='Parsed scenario DSL stored as JSON'
    )

    # Track who created this and when
    created_by = models.CharField(
        max_length=255,
        blank=True,
        help_text='Email or identifier of the user who created this scenario'
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    # Link to related risks (optional)
    risks = models.ManyToManyField(
        Risk,
        related_name='scenarios',
        blank=True,
        help_text='Risks that this scenario simulates'
    )

    class Meta:
        ordering = ['-updated_at']
        verbose_name = 'Risk Scenario'
        verbose_name_plural = 'Risk Scenarios'

    @property
    def duration(self):
        """Get scenario duration from DSL content."""
        if self.dsl_content and 'scenario' in self.dsl_content:
            return self.dsl_content['scenario'].get('duration', 0)
        return 0

    @property
    def event_count(self):
        """Get number of events in the scenario."""
        if self.dsl_content and 'events' in self.dsl_content:
            return len(self.dsl_content['events'])
        return 0

    def __str__(self):
        return f"{self.name} ({self.system.name})"
