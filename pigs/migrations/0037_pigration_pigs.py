# -*- coding: utf-8 -*-
# Generated by Django 1.10.6 on 2017-06-15 22:30
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('pigs', '0036_remove_pigsinpen_totalration'),
    ]

    operations = [
        migrations.AddField(
            model_name='pigration',
            name='pigs',
            field=models.ForeignKey(default=0, on_delete=django.db.models.deletion.CASCADE, to='pigs.Pigsinpen'),
            preserve_default=False,
        ),
    ]
