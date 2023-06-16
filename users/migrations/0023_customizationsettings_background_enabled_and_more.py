# Generated by Django 4.1.4 on 2023-03-18 21:49

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0022_customizationdata_image_alter_customizationdata_data'),
    ]

    operations = [
        migrations.AddField(
            model_name='customizationsettings',
            name='background_enabled',
            field=models.BooleanField(default=False),
        ),
        migrations.AddField(
            model_name='customizationsettings',
            name='banner_enabled',
            field=models.BooleanField(default=False),
        ),
        migrations.AddField(
            model_name='customizationsettings',
            name='banner_width_mode',
            field=models.IntegerField(choices=[(0, 'Full'), (1, 'Container')], default=1),
        ),
    ]