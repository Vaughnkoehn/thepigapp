# -*- coding: utf-8 -*-
# Generated by Django 1.10.6 on 2017-07-05 21:02
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('pigs', '0045_auto_20170705_1553'),
    ]

    operations = [
        migrations.AlterField(
            model_name='pigration',
            name='date',
            field=models.DateTimeField(blank=True),
        ),
    ]
