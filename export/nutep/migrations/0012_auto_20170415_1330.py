# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('nutep', '0011_auto_20170413_1214'),
    ]

    operations = [
        migrations.AlterField(
            model_name='userprofile',
            name='guid',
            field=models.CharField(max_length=50, null=True, blank=True),
        ),
        migrations.AlterField(
            model_name='userprofile',
            name='lines',
            field=models.ManyToManyField(to='nutep.Line', blank=True),
        ),
    ]
