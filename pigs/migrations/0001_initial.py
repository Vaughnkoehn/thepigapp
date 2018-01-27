# -*- coding: utf-8 -*-
# Generated by Django 1.11.7 on 2018-01-16 20:12
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='additives',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('additivename', models.CharField(max_length=20, unique=True)),
                ('price', models.DecimalField(decimal_places=4, max_digits=19)),
                ('amount_per_ton', models.DecimalField(decimal_places=4, max_digits=19)),
            ],
        ),
        migrations.CreateModel(
            name='Commodity',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=20, unique=True)),
                ('price', models.DecimalField(decimal_places=4, max_digits=19)),
            ],
        ),
        migrations.CreateModel(
            name='deadculled',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('dead', models.PositiveIntegerField(blank=True, null=True)),
                ('culled', models.PositiveIntegerField(blank=True, null=True)),
                ('date', models.DateTimeField(auto_now_add=True)),
            ],
        ),
        migrations.CreateModel(
            name='Pigpen',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('pen', models.CharField(max_length=2)),
            ],
        ),
        migrations.CreateModel(
            name='pigration',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('ration_price', models.DecimalField(decimal_places=4, max_digits=19)),
                ('pigsinapen', models.CharField(max_length=4)),
                ('extras', models.CharField(blank=True, max_length=15, null=True)),
                ('ration_amount', models.IntegerField()),
                ('date', models.DateTimeField(blank=True)),
                ('pigpen', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='pigs.Pigpen')),
            ],
        ),
        migrations.CreateModel(
            name='Pigsinpen',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('pigs', models.PositiveIntegerField()),
                ('pig_cost_total', models.DecimalField(decimal_places=2, max_digits=6)),
                ('date', models.DateTimeField()),
                ('notes', models.CharField(blank=True, max_length=300, null=True)),
                ('pigpen', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='pigs.Pigpen')),
            ],
        ),
        migrations.CreateModel(
            name='Ration',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('ration_number', models.CharField(max_length=15, unique=True)),
                ('ration_price', models.DecimalField(decimal_places=4, max_digits=19)),
                ('feed_per_pig', models.CharField(default=55, max_length=3)),
                ('commodity', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='pigs.Commodity', to_field='name')),
            ],
        ),
        migrations.CreateModel(
            name='Shipped',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('pigpen', models.PositiveIntegerField()),
                ('pigs', models.PositiveIntegerField()),
                ('sold_price', models.DecimalField(decimal_places=2, max_digits=6)),
                ('pig_cost', models.DecimalField(decimal_places=2, max_digits=6)),
                ('ration_amount', models.CharField(max_length=500)),
                ('pig_ration_cost', models.DecimalField(decimal_places=2, max_digits=6)),
                ('shipped_date', models.DateTimeField(auto_now_add=True)),
                ('notes', models.CharField(blank=True, max_length=300, null=True)),
            ],
        ),
        migrations.AddField(
            model_name='pigration',
            name='ration',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='pigs.Ration', to_field='ration_number'),
        ),
        migrations.AddField(
            model_name='deadculled',
            name='pigpen',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='pigs.Pigpen'),
        ),
    ]
