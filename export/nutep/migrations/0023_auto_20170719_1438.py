# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('nutep', '0022_auto_20170622_1705'),
    ]

    operations = [
        migrations.AlterField(
            model_name='terminal',
            name='guid',
            field=models.CharField(max_length=50, unique=True, null=True, db_index=True),
        ),
        migrations.AlterField(
            model_name='vessel',
            name='guid',
            field=models.CharField(max_length=50, unique=True, null=True, db_index=True),
        ),
        migrations.AlterField(
            model_name='voyage',
            name='guid',
            field=models.CharField(max_length=50, unique=True, null=True, db_index=True),
        ),
        migrations.AlterUniqueTogether(
            name='voyage',
            unique_together=set([('vessel', 'name')]),
        ),
    ]
