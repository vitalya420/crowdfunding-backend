# Generated by Django 4.1.4 on 2023-02-02 18:09

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0019_customizationdata_customizationsettings_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='customizationdata',
            name='mask',
            field=models.CharField(max_length=255),
        ),
    ]
