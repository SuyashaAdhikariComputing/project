# Generated by Django 5.0.1 on 2024-04-04 06:07

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('blog', '0008_post_image'),
    ]

    operations = [
        migrations.AlterField(
            model_name='post',
            name='image',
            field=models.ImageField(blank=True, null=True, upload_to='myimage/'),
        ),
    ]
