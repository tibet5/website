# Generated by Django 3.1.2 on 2021-02-27 01:01

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('recipients', '0052_remove_groceryrequest_can_meet_for_delivery'),
    ]

    operations = [
        migrations.AddField(
            model_name='groceryrequest',
            name='buzzer',
            field=models.CharField(blank=True, help_text='Does your building requires a buzzer code for us to contact you?', max_length=256, verbose_name='Buzzer code'),
        ),
    ]
