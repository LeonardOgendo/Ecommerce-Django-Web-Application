# Generated by Django 5.0.2 on 2024-04-19 11:53

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Core', '0022_alter_item_size_alter_item_size_category'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='item',
            name='size',
        ),
        migrations.RemoveField(
            model_name='item',
            name='size_category',
        ),
        migrations.AddField(
            model_name='orderitem',
            name='size',
            field=models.CharField(max_length=10, null=True),
        ),
        migrations.AddField(
            model_name='orderitem',
            name='size_category',
            field=models.CharField(max_length=10, null=True),
        ),
    ]
