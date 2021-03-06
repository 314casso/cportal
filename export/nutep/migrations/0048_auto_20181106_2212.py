# -*- coding: utf-8 -*-
# Generated by Django 1.11.10 on 2018-11-06 22:12
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('nutep', '0047_auto_20181105_2111'),
    ]

    operations = [
        migrations.AddField(
            model_name='file',
            name='doc_type',
            field=models.CharField(blank=True, max_length=100, null=True),
        ),
        migrations.AddField(
            model_name='file',
            name='extension',
            field=models.CharField(blank=True, max_length=10, null=True),
        ),
        migrations.AddField(
            model_name='file',
            name='guid',
            field=models.CharField(blank=True, max_length=36, null=True),
        ),
        migrations.AddField(
            model_name='file',
            name='size',
            field=models.IntegerField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='file',
            name='storage',
            field=models.CharField(blank=True, max_length=150, null=True),
        ),
    ]
