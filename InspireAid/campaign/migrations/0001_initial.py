# Generated by Django 5.0.1 on 2024-03-09 09:29

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Campaign',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=255)),
                ('description', models.TextField()),
                ('target_amount', models.DecimalField(decimal_places=2, max_digits=10)),
                ('current_amount', models.DecimalField(decimal_places=2, default=0.0, max_digits=10)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('slug', models.CharField(blank=True, max_length=130, unique=True)),
            ],
        ),
    ]
