# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models
import nutep.models


class Migration(migrations.Migration):

    dependencies = [
        ('nutep', '0013_file'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='file',
            name='image',
        ),
        migrations.AddField(
            model_name='file',
            name='file',
            field=models.FileField(null=True, upload_to=nutep.models.attachment_path, blank=True),
        ),
    ]
