# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models
import nutep.models


class Migration(migrations.Migration):

    dependencies = [
        ('nutep', '0024_auto_20170831_0920'),
    ]

    operations = [
        migrations.AddField(
            model_name='userprofile',
            name='image',
            field=models.ImageField(null=True, upload_to=nutep.models.userprofile_path, blank=True),
        ),
    ]
