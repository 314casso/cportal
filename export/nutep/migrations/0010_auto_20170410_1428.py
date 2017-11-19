# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('nutep', '0009_auto_20170410_1407'),
    ]

    operations = [
        migrations.AddField(
            model_name='uploadedtemplate',
            name='services',
            field=models.ManyToManyField(to='nutep.ServiceProvided', blank=True),
        ),
        migrations.AlterField(
            model_name='line',
            name='services',
            field=models.ManyToManyField(to='nutep.ServiceProvided', blank=True),
        ),
    ]
