# -*- coding: utf-8 -*-
# Generated by Django 1.10.6 on 2017-06-18 02:33
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('pigs', '0041_deadculled_date'),
    ]

    operations = [
        migrations.AlterField(
            model_name='deadculled',
            name='pigpen',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='pigs.Pigpen'),
        ),
    ]
