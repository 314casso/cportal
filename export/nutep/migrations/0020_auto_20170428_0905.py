# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('nutep', '0019_auto_20170423_0126'),
    ]

    operations = [
        migrations.AddField(
            model_name='file',
            name='note',
            field=models.CharField(max_length=255, null=True, blank=True),
        ),
        migrations.AlterField(
            model_name='uploadedtemplate',
            name='order',
            field=models.ForeignKey(related_name='templates', blank=True, to='nutep.Order', null=True),
        ),
    ]
