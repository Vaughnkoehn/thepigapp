# Generated by Django 2.0.1 on 2018-01-19 03:21

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('pigs', '0006_ration_sixtyeighty'),
    ]

    operations = [
        migrations.AddField(
            model_name='ration',
            name='Hit Pork',
            field=models.CharField(default=0, max_length=4),
        ),
    ]