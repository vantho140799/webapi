# Generated by Django 5.0.7 on 2024-10-08 07:37

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('home', '0018_delete_support'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='pricingplan',
            name='item',
        ),
    ]
