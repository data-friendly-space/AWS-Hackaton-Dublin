# Generated manually for Risk Simulator feature

from django.db import migrations, models
import django.db.models.deletion
import uuid


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0002_systemvisualization'),
    ]

    operations = [
        migrations.CreateModel(
            name='RiskScenario',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ('name', models.CharField(max_length=255)),
                ('description', models.TextField(blank=True)),
                ('dsl_content', models.JSONField(help_text='Parsed scenario DSL stored as JSON')),
                ('created_by', models.CharField(blank=True, help_text='Email or identifier of the user who created this scenario', max_length=255)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('system', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='scenarios', to='core.system')),
                ('risks', models.ManyToManyField(blank=True, help_text='Risks that this scenario simulates', related_name='scenarios', to='core.risk')),
            ],
            options={
                'verbose_name': 'Risk Scenario',
                'verbose_name_plural': 'Risk Scenarios',
                'ordering': ['-updated_at'],
            },
        ),
    ]
