# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models
from django.conf import settings
import django_libs.models_mixins


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Booking',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('booking_start_date', models.DateField()),
                ('booking_end_date', models.DateField()),
                ('customer_name', models.CharField(max_length=100)),
                ('phone_number', models.IntegerField()),
                ('is_approved', models.BooleanField(default=False)),
            ],
        ),
        migrations.CreateModel(
            name='BookingStatus',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('slug', models.SlugField(verbose_name='Slug')),
            ],
            options={
                'abstract': False,
            },
            bases=(django_libs.models_mixins.TranslationModelMixin, models.Model),
        ),
        migrations.CreateModel(
            name='BookingStatusTranslation',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(max_length=128, verbose_name='Name')),
                ('language_code', models.CharField(max_length=15, db_index=True)),
                ('master', models.ForeignKey(related_name='translations', editable=False, to='centers.BookingStatus')),
            ],
            options={
                'managed': True,
                'abstract': False,
                'db_table': 'centers_bookingstatus_translation',
                'db_tablespace': '',
                'default_permissions': (),
            },
        ),
        migrations.CreateModel(
            name='Center',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('price', models.IntegerField()),
                ('capacity', models.IntegerField()),
                ('description', models.TextField(default=b'', blank=True)),
                ('slug', models.SlugField(unique=True, blank=True)),
                ('name', models.CharField(max_length=100)),
                ('location', models.SmallIntegerField(default=84, choices=[(1, b'Abia'), (2, b'Abuja'), (3, b'Adamawa'), (4, b'Akwa Ibom'), (5, b'Anambra'), (6, b'Bauchi'), (7, b'Bayelsa'), (8, b'Benue'), (9, b'Borno'), (10, b'Cross River'), (11, b'Delta'), (12, b'Ebonyi'), (13, b'Edo'), (14, b'Ekiti'), (15, b'Enugu'), (16, b'Gombe'), (17, b'Imo'), (18, b'Jigawa'), (19, b'Kaduna'), (20, b'Kano'), (21, b'Katsina'), (22, b'Kebbi'), (23, b'Kogi'), (24, b'Kwara'), (25, b'Lagos'), (26, b'Nassarawa'), (27, b'Niger'), (28, b'Ogun'), (29, b'Ondo'), (30, b'Osun'), (31, b'Oyo'), (32, b'Plateau'), (33, b'Rivers'), (34, b'Sokoto'), (35, b'Taraba'), (36, b'Yobe'), (37, b'Zamfara')])),
                ('address', models.CharField(default=b'', max_length=100)),
                ('active', models.BooleanField(default=False)),
                ('date_created', models.DateField(auto_now_add=True)),
                ('date_last_modified', models.DateField(auto_now=True)),
                ('image', models.ImageField(null=True, upload_to=b'center_images')),
                ('is_available', models.BooleanField()),
                ('owner', models.ForeignKey(to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.AddField(
            model_name='booking',
            name='center',
            field=models.ForeignKey(to='centers.Center'),
        ),
        migrations.AddField(
            model_name='booking',
            name='owner',
            field=models.ForeignKey(to=settings.AUTH_USER_MODEL),
        ),
        migrations.AlterUniqueTogether(
            name='bookingstatustranslation',
            unique_together=set([('language_code', 'master')]),
        ),
    ]
