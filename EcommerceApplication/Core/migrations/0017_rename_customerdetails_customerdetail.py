# Generated by Django 5.0.2 on 2024-03-31 10:09

from django.conf import settings
from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('Core', '0016_rename_delivery_address_customerdetails_pickup_station_and_more'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.RenameModel(
            old_name='CustomerDetails',
            new_name='CustomerDetail',
        ),
    ]
