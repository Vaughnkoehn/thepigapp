# Generated by Django 2.0.1 on 2018-01-18 16:20

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('pigs', '0002_auto_20180118_1005'),
    ]

    operations = [
        migrations.AddField(
            model_name='ration',
            name='dynamin',
            field=models.CharField(default=0, max_length=4),
        ),
    ]
