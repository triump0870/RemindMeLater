# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('Reminder', '0002_reminder_channel'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='reminder',
            name='channel',
        ),
    ]
