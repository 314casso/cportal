# -*- coding: utf-8 -*-
# Generated by Django 1.11.10 on 2018-12-06 11:46
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('contract', '0013_clientorder_data_event'),
    ]

    operations = [
        migrations.AlterField(
            model_name='clientorder',
            name='event',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='orderevents', to='nutep.DateQueryEvent'),
        ),
    ]
