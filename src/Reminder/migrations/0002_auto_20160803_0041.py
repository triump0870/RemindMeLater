# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import timezone_field.fields


class Migration(migrations.Migration):

    dependencies = [
        ('Reminder', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='reminder',
            name='task_id',
            field=models.CharField(max_length=50, editable=False, blank=True),
        ),
        migrations.AddField(
            model_name='reminder',
            name='time_zone',
            field=timezone_field.fields.TimeZoneField(default=b'Asia/Kolkata'),
        ),
    ]
