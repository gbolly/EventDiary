# -*- coding: utf-8 -*-
# Generated by Django 1.10.2 on 2017-01-10 15:17
from __future__ import unicode_literals

from django.db import migrations, models
import web.centers.models


class Migration(migrations.Migration):

    dependencies = [
        ('centers', '0004_auto_20170110_0844'),
    ]

    operations = [
        migrations.AddField(
            model_name='center',
            name='commission',
            field=models.CharField(default='0.5%', max_length=10, validators=[web.centers.models.valid_pct]),
            preserve_default=False,
        ),
    ]
