# Generated by Django 4.1.5 on 2024-03-12 13:43

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('utils', '0001_initial'),
        ('club', '0005_remove_roadmap_club_id_club_roadmap'),
    ]

    operations = [
        migrations.AlterField(
            model_name='roadmapweek',
            name='roadmap_id',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='weeks', to='club.roadmap'),
        ),
        migrations.CreateModel(
            name='ClubReview',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('review', models.CharField(max_length=500, unique=True)),
                ('rating', models.FloatField(default='0.0')),
                ('club_id', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='reviews', to='club.club')),
                ('user_id', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='utils.user')),
            ],
            options={
                'verbose_name': 'ClubReview',
                'verbose_name_plural': 'ClubReviews',
                'db_table': 'club_review',
            },
        ),
    ]