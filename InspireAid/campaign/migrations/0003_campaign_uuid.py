# Generated by Django 5.0.1 on 2024-03-26 05:28

import uuid
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('campaign', '0002_campaign_author'),
    ]

    operations = [
        migrations.AddField(
            model_name='campaign',
            name='uuid',
            field=models.UUIDField(default=uuid.uuid4, editable=False, unique=True),
        ),
    ]
