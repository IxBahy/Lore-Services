# Generated by Django 4.1.5 on 2024-05-04 21:33

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('club', '0010_alter_roadmapweek_description_and_more'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='roadmapweek',
            name='week_number',
        ),
        migrations.AddField(
            model_name='club',
            name='category',
            field=models.CharField(default='General', max_length=250),
        ),
    ]
