# -*- coding: utf-8 -*-
# Generated by Django 1.10.6 on 2017-06-02 22:48
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('pigs', '0016_auto_20170602_1748'),
    ]

    operations = [
        migrations.AlterField(
            model_name='ration',
            name='ration_price',
            field=models.IntegerField(),
        ),
    ]
