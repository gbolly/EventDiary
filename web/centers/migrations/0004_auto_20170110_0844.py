# -*- coding: utf-8 -*-
# Generated by Django 1.10.2 on 2017-01-10 08:44
from __future__ import unicode_literals

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('centers', '0003_auto_20170109_2343'),
    ]

    operations = [
        migrations.RenameField(
            model_name='localgovarea',
            old_name='local_gov',
            new_name='name',
        ),
        migrations.RenameField(
            model_name='state',
            old_name='state',
            new_name='name',
        ),
    ]
