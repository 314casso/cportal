# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('nutep', '0008_auto_20170410_1404'),
    ]

    operations = [
        migrations.AlterField(
            model_name='serviceprovided',
            name='service',
            field=models.IntegerField(db_index=True, unique=True, choices=[(1, '\u042d\u043a\u0441\u043f\u043e\u0440\u0442\u043d\u044b\u0435 \u043f\u043e\u0440\u0443\u0447\u0435\u043d\u0438\u044f')]),
        ),
    ]
