# -*- coding: utf-8 -*-
# Generated by Django 1.11.10 on 2018-04-19 14:57
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('nutep', '0043_auto_20180413_1137'),
    ]

    operations = [
        migrations.AlterField(
            model_name='employee',
            name='mobile',
            field=models.CharField(blank=True, max_length=50, verbose_name='mobile'),
        ),
        migrations.AlterField(
            model_name='employee',
            name='phone',
            field=models.CharField(blank=True, max_length=50, null=True, verbose_name='phone'),
        ),
        migrations.AlterField(
            model_name='employee',
            name='skype',
            field=models.CharField(blank=True, max_length=50, null=True, verbose_name='skype'),
        ),
    ]
