# Generated by Django 4.1.4 on 2023-05-18 22:20

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('store', '0002_cart_destinationaddress_cartitem_cart_goods_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='destinationaddress',
            name='user',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL),
        ),
    ]
