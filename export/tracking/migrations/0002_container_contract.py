# -*- coding: utf-8 -*-
# Generated by Django 1.11.10 on 2018-11-09 09:09
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('tracking', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='container',
            name='contract',
            field=models.CharField(blank=True, db_index=True, max_length=50, null=True),
        ),
    ]