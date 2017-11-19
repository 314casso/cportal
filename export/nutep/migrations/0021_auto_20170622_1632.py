# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('nutep', '0020_auto_20170428_0905'),
    ]

    operations = [
        migrations.AlterField(
            model_name='readiness',
            name='type',
            field=models.CharField(max_length=4, db_index=True),
        ),
    ]
