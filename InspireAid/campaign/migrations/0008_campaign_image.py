# Generated by Django 5.0.1 on 2024-04-04 06:57

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('campaign', '0007_alter_campaign_description'),
    ]

    operations = [
        migrations.AddField(
            model_name='campaign',
            name='image',
            field=models.ImageField(blank=True, null=True, upload_to='myimage/'),
        ),
    ]
