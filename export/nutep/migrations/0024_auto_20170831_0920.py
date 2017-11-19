# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('nutep', '0023_auto_20170719_1438'),
    ]

    operations = [
        migrations.AddField(
            model_name='mission',
            name='issue_date',
            field=models.DateTimeField(null=True, blank=True),
        ),
        migrations.AddField(
            model_name='mission',
            name='reception_date',
            field=models.DateTimeField(null=True, blank=True),
        ),
    ]
