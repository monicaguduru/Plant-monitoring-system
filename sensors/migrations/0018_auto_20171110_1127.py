# -*- coding: utf-8 -*-
# Generated by Django 1.11.4 on 2017-11-10 05:57
from __future__ import unicode_literals

from django.db import migrations, models
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('sensors', '0017_remove_b_name'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='c',
            name='plantId',
        ),
        migrations.AddField(
            model_name='b',
            name='name',
            field=models.CharField(default=django.utils.timezone.now, max_length=255),
            preserve_default=False,
        ),
        migrations.DeleteModel(
            name='c',
        ),
    ]
