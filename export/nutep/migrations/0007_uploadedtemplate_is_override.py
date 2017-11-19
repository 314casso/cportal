# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('nutep', '0006_uploadedtemplate_md5_hash'),
    ]

    operations = [
        migrations.AddField(
            model_name='uploadedtemplate',
            name='is_override',
            field=models.BooleanField(default=False),
        ),
    ]
