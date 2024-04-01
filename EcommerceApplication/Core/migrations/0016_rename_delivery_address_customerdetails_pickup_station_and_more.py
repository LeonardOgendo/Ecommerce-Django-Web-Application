# Generated by Django 5.0.2 on 2024-03-31 10:00

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Core', '0015_customerdetails'),
    ]

    operations = [
        migrations.RenameField(
            model_name='customerdetails',
            old_name='delivery_address',
            new_name='pickup_station',
        ),
        migrations.AlterUniqueTogether(
            name='customerdetails',
            unique_together=set(),
        ),
        migrations.AddField(
            model_name='customerdetails',
            name='surname',
            field=models.CharField(max_length=100, null=True),
        ),
        migrations.AlterField(
            model_name='customerdetails',
            name='country',
            field=models.CharField(max_length=100),
        ),
        migrations.AlterField(
            model_name='customerdetails',
            name='first_name',
            field=models.CharField(max_length=100),
        ),
        migrations.AlterField(
            model_name='customerdetails',
            name='town',
            field=models.CharField(max_length=100),
        ),
        migrations.RemoveField(
            model_name='customerdetails',
            name='last_name',
        ),
    ]
