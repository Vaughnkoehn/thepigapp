# -*- coding: utf-8 -*-
# Generated by Django 1.10.6 on 2017-06-13 02:24
from __future__ import unicode_literals

import django.core.validators
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('pigs', '0030_pigsinpen_pig_ration_cost'),
    ]

    operations = [
        migrations.AlterField(
            model_name='pigsinpen',
            name='pigs',
            field=models.IntegerField(default=1, validators=[django.core.validators.MinValueValidator(0)]),
        ),
    ]
