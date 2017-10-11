# -*- coding: utf-8 -*-
# Generated by Django 1.11.5 on 2017-10-11 19:58
from __future__ import unicode_literals

from django.db import migrations
from antispam.utils import normalize_email


def normalize(apps, schema_editor):
    User = apps.get_model('account', 'User')
    for user in User.objects.exclude(email=''):
        user.normalized_email = normalize_email(user.email)
        user.save()


class Migration(migrations.Migration):

    dependencies = [
        ('account', '0015_user_normalized_email'),
    ]

    operations = [
        migrations.RunPython(normalize),
    ]
