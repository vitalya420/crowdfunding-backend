# Generated by Django 4.1.4 on 2023-01-27 03:04

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0014_user_activity'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='user',
            name='profile_type',
        ),
    ]
