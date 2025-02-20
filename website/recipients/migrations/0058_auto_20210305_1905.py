# Generated by Django 3.1.2 on 2021-03-06 00:05

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('recipients', '0057_auto_20210303_1805'),
    ]

    operations = [
        migrations.AddField(
            model_name='groceryrequest',
            name='physical_gift_card',
            field=models.BooleanField(default=False, help_text='By default we will send a digital gift card to the email account you provided, if you would prefer a physical gift card check here.', verbose_name='Physical gift card'),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='groceryrequest',
            name='gift_card',
            field=models.CharField(choices=[('Walmart', 'Walmart'), ("President's Choice", 'Presidents Choice'), ('Food Share', 'Food Share')], help_text='What type of gift card would you want?', max_length=256, verbose_name='Gift card'),
        ),
    ]
