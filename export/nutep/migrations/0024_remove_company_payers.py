# -*- coding: utf-8 -*-
# Generated by Django 1.11.9 on 2018-02-13 09:49
from __future__ import unicode_literals

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('nutep', '0023_auto_20180212_1711'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='company',
            name='payers',
        ),
    ]
