# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import django.core.validators


class Migration(migrations.Migration):

    dependencies = [
        ('Reminder', '0004_auto_20160806_1410'),
    ]

    operations = [
        migrations.AlterField(
            model_name='reminder',
            name='phone_number',
            field=models.CharField(blank=True, max_length=15, null=True, validators=[django.core.validators.RegexValidator(regex=b'^\\+?1?\\d{12,15}$', message=b"Phone number must be entered in the format: '+919876543210'. Up to 15 digits allowed.", code=b'Invalid Phone number')]),
        ),
    ]
