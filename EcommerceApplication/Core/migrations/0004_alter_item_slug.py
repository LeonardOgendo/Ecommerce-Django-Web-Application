# Generated by Django 5.0.2 on 2024-03-18 05:46

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Core', '0003_item_slug_alter_item_price'),
    ]

    operations = [
        migrations.AlterField(
            model_name='item',
            name='slug',
            field=models.SlugField(default='product1'),
            preserve_default=False,
        ),
    ]
