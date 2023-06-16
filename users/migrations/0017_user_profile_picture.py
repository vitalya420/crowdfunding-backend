# Generated by Django 4.1.4 on 2023-01-27 18:06

from django.db import migrations, models
import users.models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0016_subtier_description'),
    ]

    operations = [
        migrations.AddField(
            model_name='user',
            name='profile_picture',
            field=models.ImageField(blank=True, null=True, upload_to=users.models.upload_to),
        ),
    ]
