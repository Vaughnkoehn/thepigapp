# Generated by Django 2.0.1 on 2018-02-15 16:16

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('pigs', '0006_auto_20180212_2000'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='ration',
            options={'ordering': ['feed_per_pig']},
        ),
        migrations.AlterField(
            model_name='pigration',
            name='id',
            field=models.PositiveIntegerField(primary_key=True, serialize=False),
        ),
    ]