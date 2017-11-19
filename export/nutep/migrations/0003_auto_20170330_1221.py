# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('nutep', '0002_auto_20170323_1613'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='baseerror',
            options={'ordering': ('id',), 'verbose_name': '\u041e\u0448\u0438\u0431\u043a\u0430', 'verbose_name_plural': '\u041e\u0448\u0438\u0431\u043a\u0438'},
        ),
    ]
