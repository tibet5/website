# Generated by Django 3.1.2 on 2020-11-08 21:39

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('recipients', '0003_auto_20201108_2132'),
    ]

    operations = [
        migrations.AlterField(
            model_name='mealrequest',
            name='requester_email',
            field=models.EmailField(blank=True, max_length=254, verbose_name='Your email address'),
        ),
        migrations.AlterField(
            model_name='mealrequest',
            name='requester_name',
            field=models.CharField(blank=True, max_length=256, verbose_name='Your full name'),
        ),
        migrations.AlterField(
            model_name='mealrequest',
            name='requester_phone_number',
            field=models.CharField(blank=True, help_text='Use the format 555-555-5555', max_length=20, verbose_name='Your phone number'),
        ),
    ]
