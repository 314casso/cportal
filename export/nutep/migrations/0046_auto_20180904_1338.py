# -*- coding: utf-8 -*-
# Generated by Django 1.11.10 on 2018-09-04 13:38
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('nutep', '0045_auto_20180618_1130'),
    ]

    operations = [
        migrations.AlterField(
            model_name='clientservice',
            name='type',
            field=models.IntegerField(choices=[(1, '\u0412\u0437\u0430\u0438\u043c\u043e\u0440\u0430\u0441\u0447\u0435\u0442\u044b'), (2, '\u0421\u043b\u0435\u0436\u0435\u043d\u0438\u0435'), (3, '\u042d\u043a\u0441\u043f\u043e\u0440\u0442 \u043d\u0430 \u0442\u0435\u0440\u043c\u0438\u043d\u0430\u043b\u0435'), (4, '\u0424\u043e\u0442\u043e \u043a\u043e\u043d\u0442\u0435\u0439\u043d\u0435\u0440\u043e\u0432'), (5, '\u0421\u0442\u043e\u043a \u043f\u043e\u0440\u043e\u0436\u043d\u0438\u0445')], unique=True),
        ),
        migrations.AlterField(
            model_name='datequeryevent',
            name='type',
            field=models.IntegerField(blank=True, choices=[(1, '\u0412\u0437\u0430\u0438\u043c\u043e\u0440\u0430\u0441\u0447\u0435\u0442\u044b'), (2, '\u0421\u043b\u0435\u0436\u0435\u043d\u0438\u0435'), (3, '\u042d\u043a\u0441\u043f\u043e\u0440\u0442 \u043d\u0430 \u0442\u0435\u0440\u043c\u0438\u043d\u0430\u043b\u0435'), (4, '\u0424\u043e\u0442\u043e \u043a\u043e\u043d\u0442\u0435\u0439\u043d\u0435\u0440\u043e\u0432'), (5, '\u0421\u0442\u043e\u043a \u043f\u043e\u0440\u043e\u0436\u043d\u0438\u0445')], null=True),
        ),
    ]
