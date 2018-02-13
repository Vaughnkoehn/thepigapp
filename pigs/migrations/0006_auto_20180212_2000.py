# Generated by Django 2.0.1 on 2018-02-13 02:00

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('pigs', '0005_auto_20180211_1722'),
    ]

    operations = [
        migrations.CreateModel(
            name='breed',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('date', models.DateField()),
            ],
        ),
        migrations.RemoveField(
            model_name='status',
            name='Sow',
        ),
        migrations.RemoveField(
            model_name='status',
            name='by_boar',
        ),
        migrations.RemoveField(
            model_name='status',
            name='status',
        ),
        migrations.AddField(
            model_name='sows',
            name='bred',
            field=models.NullBooleanField(),
        ),
        migrations.AddField(
            model_name='sows',
            name='farrowing',
            field=models.NullBooleanField(),
        ),
        migrations.DeleteModel(
            name='status',
        ),
        migrations.DeleteModel(
            name='statusoptions',
        ),
        migrations.AddField(
            model_name='breed',
            name='Sow',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='pigs.Sows'),
        ),
        migrations.AddField(
            model_name='breed',
            name='by_boar',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='pigs.boars'),
        ),
    ]