# Generated by Django 4.1.4 on 2023-01-23 01:41

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0003_remove_user_fullname_user_accounts'),
    ]

    operations = [
        migrations.AlterField(
            model_name='user',
            name='accounts',
            field=models.ManyToManyField(to='users.account'),
        ),
    ]
