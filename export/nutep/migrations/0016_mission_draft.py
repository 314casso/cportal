# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('nutep', '0015_mission'),
    ]

    operations = [
        migrations.AddField(
            model_name='mission',
            name='draft',
            field=models.ForeignKey(related_name='missions', default=1, to='nutep.Draft'),
            preserve_default=False,
        ),
    ]
