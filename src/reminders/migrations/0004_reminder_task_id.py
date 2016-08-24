# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('reminders', '0003_auto_20160817_0520'),
    ]

    operations = [
        migrations.AddField(
            model_name='reminder',
            name='task_id',
            field=models.CharField(max_length=50, editable=False, blank=True),
        ),
    ]
