# Generated by Django 3.1.2 on 2020-12-05 01:12

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('volunteers', '0011_auto_20201203_2239'),
    ]

    operations = [
        migrations.AlterField(
            model_name='volunteer',
            name='anonymized_latitude',
            field=models.FloatField(blank=True, default=43.65107),
        ),
        migrations.AlterField(
            model_name='volunteer',
            name='anonymized_longitude',
            field=models.FloatField(blank=True, default=-79.347015),
        ),
    ]
