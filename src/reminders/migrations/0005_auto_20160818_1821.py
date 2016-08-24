# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('reminders', '0004_reminder_task_id'),
    ]

    operations = [
        migrations.AlterField(
            model_name='reminder',
            name='completed',
            field=models.BooleanField(default=False, editable=False),
        ),
    ]
