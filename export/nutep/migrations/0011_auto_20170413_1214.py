# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('nutep', '0010_auto_20170410_1428'),
    ]

    operations = [
        migrations.AlterField(
            model_name='serviceprovided',
            name='service',
            field=models.CharField(db_index=True, unique=True, max_length=5, choices=[(b'00001', '\u042d\u043a\u0441\u043f\u043e\u0440\u0442\u043d\u044b\u0435 \u043f\u043e\u0440\u0443\u0447\u0435\u043d\u0438\u044f')]),
        ),
    ]
