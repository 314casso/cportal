# -*- coding: utf-8 -*-
# Generated by Django 1.11.10 on 2018-12-05 16:58
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('contract', '0008_clientorder'),
    ]

    operations = [
        migrations.AlterField(
            model_name='clientorder',
            name='contracts',
            field=models.ManyToManyField(related_name='orders', to='contract.Contract'),
        ),
    ]
