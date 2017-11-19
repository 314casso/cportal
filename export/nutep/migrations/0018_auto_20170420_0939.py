# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('nutep', '0017_auto_20170419_1440'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='order',
            options={'verbose_name': '\u0417\u0430\u044f\u0432\u043a\u0430', 'verbose_name_plural': '\u0417\u0430\u044f\u0432\u043a\u0438'},
        ),
        migrations.RenameField(
            model_name='voyage',
            old_name='etd',
            new_name='eta',
        ),
    ]
