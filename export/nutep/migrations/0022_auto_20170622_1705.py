# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('nutep', '0021_auto_20170622_1632'),
    ]

    operations = [
        migrations.AlterField(
            model_name='container',
            name='type',
            field=models.CharField(max_length=4, db_index=True),
        ),
    ]
