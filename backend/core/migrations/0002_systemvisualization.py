# Generated migration for SystemVisualization model

import uuid
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='SystemVisualization',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ('dot_code', models.TextField(help_text='Generated Graphviz DOT code')),
                ('data_hash', models.CharField(help_text='SHA256 hash of system data to detect changes', max_length=64)),
                ('generated_at', models.DateTimeField(auto_now=True)),
                ('system', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, related_name='visualization', to='core.system')),
            ],
            options={
                'verbose_name': 'System Visualization',
                'verbose_name_plural': 'System Visualizations',
            },
        ),
    ]
