# -*- coding: utf-8 -*-
# Generated by Django 1.11.9 on 2018-01-06 14:03
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('nutep', '0012_userprofile_details'),
    ]

    operations = [
        migrations.AddField(
            model_name='userprofile',
            name='ukt_id',
            field=models.CharField(blank=True, max_length=36, null=True),
        ),
    ]
