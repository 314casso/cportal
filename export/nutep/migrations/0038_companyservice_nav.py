# -*- coding: utf-8 -*-
# Generated by Django 1.11.10 on 2018-04-06 12:08
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('nutep', '0037_company_dashboard_view'),
    ]

    operations = [
        migrations.AddField(
            model_name='companyservice',
            name='nav',
            field=models.CharField(blank=True, max_length=150, null=True),
        ),
    ]
