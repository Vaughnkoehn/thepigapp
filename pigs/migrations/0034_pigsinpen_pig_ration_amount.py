# -*- coding: utf-8 -*-
# Generated by Django 1.10.6 on 2017-06-15 21:47
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('pigs', '0033_shipped'),
    ]

    operations = [
        migrations.AddField(
            model_name='pigsinpen',
            name='pig_ration_amount',
            field=models.CharField(blank=True, max_length=500, null=True),
        ),
    ]
