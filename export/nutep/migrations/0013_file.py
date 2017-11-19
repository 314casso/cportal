# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models
import nutep.models


class Migration(migrations.Migration):

    dependencies = [
        ('contenttypes', '0002_remove_content_type_name'),
        ('nutep', '0012_auto_20170415_1330'),
    ]

    operations = [
        migrations.CreateModel(
            name='File',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('object_id', models.PositiveIntegerField()),
                ('title', models.CharField(max_length=255, null=True, blank=True)),
                ('image', models.ImageField(null=True, upload_to=nutep.models.attachment_path, blank=True)),
                ('content_type', models.ForeignKey(to='contenttypes.ContentType')),
            ],
        ),
    ]
