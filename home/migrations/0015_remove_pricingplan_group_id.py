# Generated by Django 5.0.7 on 2024-10-03 04:13

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('home', '0014_pricingplan_group_id'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='pricingplan',
            name='group_id',
        ),
    ]
