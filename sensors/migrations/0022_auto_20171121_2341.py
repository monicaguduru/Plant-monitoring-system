# -*- coding: utf-8 -*-
# Generated by Django 1.11.4 on 2017-11-21 18:11
from __future__ import unicode_literals

from django.db import migrations, models
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('sensors', '0021_auto_20171110_1159'),
    ]

    operations = [
        migrations.RenameField(
            model_name='plantid',
            old_name='name',
            new_name='cityname',
        ),
        migrations.RemoveField(
            model_name='plantid',
            name='plantId',
        ),
        migrations.AddField(
            model_name='plantid',
            name='latitude',
            field=models.CharField(default=django.utils.timezone.now, max_length=50),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='plantid',
            name='longitude',
            field=models.CharField(default=django.utils.timezone.now, max_length=50),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='plantid',
            name='plantname',
            field=models.CharField(default=django.utils.timezone.now, max_length=255),
            preserve_default=False,
        ),
        migrations.DeleteModel(
            name='stationlocation',
        ),
    ]