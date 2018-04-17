# -*- coding: utf-8 -*-
# Generated by Django 1.11.10 on 2018-04-17 12:22
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('nutep', '0043_auto_20180413_1137'),
        ('terminal_export', '0002_auto_20180416_1510'),
    ]

    operations = [
        migrations.AddField(
            model_name='terminalexport',
            name='nomenclature',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='nutep.Nomenclature'),
        ),
        migrations.AlterField(
            model_name='stuffing',
            name='container',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='stuffs', to='terminal_export.Container'),
        ),
    ]
