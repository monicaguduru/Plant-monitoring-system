# -*- coding: utf-8 -*-
# Generated by Django 1.11.4 on 2017-08-30 05:47
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('sensors', '0002_album_is_favourite'),
    ]

    operations = [
        migrations.CreateModel(
            name='Sensors',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('sensor1', models.FloatField(default=0)),
                ('sensor2', models.FloatField(default=0)),
            ],
        ),
    ]
