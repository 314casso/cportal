# -*- coding: utf-8 -*-
# Generated by Django 1.11.10 on 2019-10-25 11:59
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('terminal_export', '0012_container_dateout'),
    ]

    operations = [
        migrations.AlterField(
            model_name='container',
            name='dateout',
            field=models.DateTimeField(blank=True, null=True),
        ),
    ]
