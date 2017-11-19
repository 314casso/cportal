# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('nutep', '0003_auto_20170330_1221'),
    ]

    operations = [
        migrations.AlterField(
            model_name='uploadedtemplate',
            name='status',
            field=models.IntegerField(default=1, blank=True, db_index=True, choices=[(1, '\u041d\u043e\u0432\u044b\u0439'), (2, '\u0412 \u043e\u0431\u0440\u0430\u0431\u043e\u0442\u043a\u0435'), (3, '\u041e\u0431\u0440\u0430\u0431\u043e\u0442\u0430\u043d'), (500, '\u041e\u0448\u0438\u0431\u043a\u0430'), (4, '\u041e\u0431\u043d\u043e\u0432\u043b\u0435\u043d\u0438\u0435')]),
        ),
    ]
