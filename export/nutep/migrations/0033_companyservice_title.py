# -*- coding: utf-8 -*-
# Generated by Django 1.11.10 on 2018-04-04 14:57
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('nutep', '0032_auto_20180404_1454'),
    ]

    operations = [
        migrations.AddField(
            model_name='companyservice',
            name='title',
            field=models.CharField(blank=True, max_length=150, null=True),
        ),
    ]