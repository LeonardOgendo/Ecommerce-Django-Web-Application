# Generated by Django 5.0.2 on 2024-03-22 09:15

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Core', '0007_alter_item_description'),
    ]

    operations = [
        migrations.AddField(
            model_name='orderitem',
            name='quantity',
            field=models.IntegerField(default=1),
        ),
    ]