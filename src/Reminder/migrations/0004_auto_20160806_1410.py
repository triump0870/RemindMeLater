# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import django.core.validators


class Migration(migrations.Migration):

    dependencies = [
        ('Reminder', '0003_remove_reminder_channel'),
    ]

    operations = [
        migrations.AlterField(
            model_name='reminder',
            name='phone_number',
            field=models.CharField(blank=True, max_length=15, null=True, validators=[django.core.validators.RegexValidator(regex=b'^\\+?1?\\d{9,15}$', message=b"Phone number must be entered in the format: '+919876543210'. Up to 15 digits allowed.")]),
        ),
    ]
