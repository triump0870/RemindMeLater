# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('Reminder', '0002_reminder_channel'),
    ]

    operations = [
        migrations.AlterField(
            model_name='reminder',
            name='channel',
            field=models.CharField(default=2, max_length=1, blank=True, choices=[(1, b'PHONE NUMBER'), (2, b'EMAIL')]),
        ),
    ]
