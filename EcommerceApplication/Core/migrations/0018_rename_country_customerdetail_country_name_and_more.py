# Generated by Django 5.0.2 on 2024-03-31 12:09

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Core', '0017_rename_customerdetails_customerdetail'),
    ]

    operations = [
        migrations.RenameField(
            model_name='customerdetail',
            old_name='country',
            new_name='country_name',
        ),
        migrations.AddField(
            model_name='customerdetail',
            name='country_code',
            field=models.CharField(max_length=2, null=True),
        ),
    ]
