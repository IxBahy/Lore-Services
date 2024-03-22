# Generated by Django 4.1.5 on 2024-03-17 15:36

from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('utils', '0004_alter_user_managers_alter_user_email_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='user',
            name='friends',
            field=models.ManyToManyField(null=True, related_name='friends', to=settings.AUTH_USER_MODEL),
        ),
    ]