# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('nutep', '0005_auto_20170407_1437'),
    ]

    operations = [
        migrations.AddField(
            model_name='uploadedtemplate',
            name='md5_hash',
            field=models.CharField(db_index=True, max_length=32, null=True, verbose_name=b'md5 hash', blank=True),
        ),
    ]
