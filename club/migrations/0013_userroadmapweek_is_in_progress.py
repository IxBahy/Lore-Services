# Generated by Django 4.1.5 on 2024-05-17 15:48

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('club', '0012_club_created_at'),
    ]

    operations = [
        migrations.AddField(
            model_name='userroadmapweek',
            name='is_in_progress',
            field=models.BooleanField(default=False),
        ),
    ]
