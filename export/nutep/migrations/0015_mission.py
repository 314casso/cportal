# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('nutep', '0014_auto_20170415_2035'),
    ]

    operations = [
        migrations.CreateModel(
            name='Mission',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(max_length=12, db_index=True)),
                ('guid', models.CharField(max_length=50)),
            ],
            options={
                'ordering': ('name',),
                'verbose_name': '\u041f\u043e\u0440\u0443\u0447\u0435\u043d\u0438\u0435',
                'verbose_name_plural': '\u041f\u043e\u0440\u0443\u0447\u0435\u043d\u0438\u044f',
            },
        ),
    ]
