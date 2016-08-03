# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import timezone_field.fields


class Migration(migrations.Migration):

    dependencies = [
        ('Reminder', '0003_auto_20160803_0210'),
    ]

    operations = [
        migrations.AlterField(
            model_name='reminder',
            name='time_zone',
            field=timezone_field.fields.TimeZoneField(default=b'Asia/Kolkata'),
        ),
    ]
