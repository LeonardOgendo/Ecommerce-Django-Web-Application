# Generated by Django 5.0.2 on 2024-03-10 13:03

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Core', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='item',
            name='item_image',
            field=models.ImageField(null=True, upload_to='images/'),
        ),
    ]
