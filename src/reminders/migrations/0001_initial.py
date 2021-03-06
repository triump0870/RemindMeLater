# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import timezone_field.fields
import django.core.validators


class Migration(migrations.Migration):

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Reminder',
            fields=[
                ('id', models.AutoField(verbose_name='ID',
                                        serialize=False, auto_created=True, primary_key=True)),
                ('task_id', models.CharField(
                    max_length=50, editable=False, blank=True)),
                ('message', models.CharField(max_length=500)),
                ('date', models.DateField()),
                ('time', models.TimeField()),
                ('created', models.DateTimeField(auto_now_add=True)),
                ('phone_number', models.CharField(blank=True, max_length=15, null=True, validators=[django.core.validators.RegexValidator(
                    regex=b'^\\+?1?\\d{12,15}$', message=b"Phone number must be entered in the format: '+919876543210'. Up to 15 digits allowed.", code=b'Invalid Phone number')])),
                ('email', models.EmailField(max_length=100, null=True, blank=True)),
                ('completed', models.BooleanField(default=False)),
                ('time_zone', timezone_field.fields.TimeZoneField(
                    default=b'Asia/Kolkata')),
            ],
        ),
    ]
