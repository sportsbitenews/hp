# -*- coding: utf-8 -*-
# Generated by Django 1.10.1 on 2016-10-07 08:15
from __future__ import unicode_literals

from django.db import migrations
import jsonfield.fields


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0006_auto_20161002_1140'),
    ]

    operations = [
        migrations.AddField(
            model_name='addressactivity',
            name='headers',
            field=jsonfield.fields.JSONField(default=dict, help_text='Request headers used.'),
        ),
    ]
