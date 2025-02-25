# Generated by Django 3.1.2 on 2020-11-16 03:01

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('auth', '0012_alter_user_first_name_max_length'),
    ]

    operations = [
        migrations.CreateModel(
            name='Volunteer',
            fields=[
                ('user', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, primary_key=True, related_name='volunteer', serialize=False, to='auth.user')),
                ('address_1', models.CharField(blank=True, help_text='Street name and number', max_length=256, verbose_name='Address line 1')),
                ('address_2', models.CharField(blank=True, help_text='Apartment, Unit, or Suite number', max_length=256, verbose_name='Address line 2')),
                ('city', models.CharField(choices=[('Ajax', 'Ajax'), ('Aurora', 'Aurora'), ('Brampton', 'Brampton'), ('Brock', 'Brock'), ('Burlington', 'Burlington'), ('Caledon', 'Caledon'), ('Clarington', 'Clarington'), ('East Gwilimbury', 'East Gwilimbury'), ('East York', 'East York'), ('Etobicoke', 'Etobicoke'), ('Georgina', 'Georgina'), ('Halton Hills', 'Halton Hills'), ('Hamilton', 'Hamilton'), ('King', 'King'), ('Maple', 'Maple'), ('Markham', 'Markham'), ('Milton', 'Milton'), ('Mississauga', 'Mississauga'), ('Newmarket', 'Newmarket'), ('North York', 'North York'), ('Oakville', 'Oakville'), ('Oshawa', 'Oshawa'), ('Pickering', 'Pickering'), ('Richmond Hill', 'Richmond Hill'), ('Scarborough', 'Scarborough'), ('Scugog', 'Scugog'), ('Stouffville', 'Stouffville'), ('Thornhill', 'Thornhill'), ('Toronto', 'Toronto (downtown, east/west ends)'), ('Uxbridge', 'Uxbridge'), ('Vaughan', 'Vaughan'), ('Whitby', 'Whitby'), ('York', 'York')], default='Toronto', max_length=50, verbose_name='City')),
                ('postal_code', models.CharField(blank=True, max_length=7, verbose_name='Postal code')),
                ('is_coordinator', models.BooleanField(verbose_name='Volunteer Coordinator')),
                ('is_driver', models.BooleanField(verbose_name='Driver')),
                ('is_chef', models.BooleanField(verbose_name='Chef')),
                ('training_complete', models.BooleanField(verbose_name='Training Complete')),
            ],
        ),
    ]
