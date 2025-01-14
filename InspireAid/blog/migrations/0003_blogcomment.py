# Generated by Django 5.0.1 on 2024-03-26 12:40

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('blog', '0002_alter_post_author'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='BlogComment',
            fields=[
                ('sno', models.AutoField(primary_key=True, serialize=False)),
                ('comment', models.TextField()),
                ('date', models.DateTimeField(auto_now_add=True)),
                ('Blog_post', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='comments', to='blog.post')),
                ('comment_author', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
                ('parent', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='blog.blogcomment')),
            ],
        ),
    ]
