# Generated by Django 3.1.2 on 2020-11-19 03:01

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('volunteers', '0004_volunteerapplication'),
    ]

    operations = [
        migrations.AddConstraint(
            model_name='volunteerapplication',
            constraint=models.UniqueConstraint(fields=('user', 'role'), name='unique role per user application'),
        ),
    ]
