# Generated by Django 5.0.1 on 2024-04-08 07:55

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('volunteers', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='volunteercampaign',
            name='image',
            field=models.ImageField(blank=True, null=True, upload_to='volunteer_campaign_images/'),
        ),
    ]
