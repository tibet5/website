# Generated by Django 3.1.2 on 2020-12-04 03:01

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('recipients', '0031_containerdeliverycomment_groceryrequestcomment_mealdeliverycomment_mealrequestcomment'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='containerdeliverycomment',
            name='author',
        ),
        migrations.RemoveField(
            model_name='containerdeliverycomment',
            name='subject',
        ),
        migrations.DeleteModel(
            name='ContainerDelivery',
        ),
        migrations.DeleteModel(
            name='ContainerDeliveryComment',
        ),
    ]
