# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('nutep', '0007_uploadedtemplate_is_override'),
    ]

    operations = [
        migrations.CreateModel(
            name='ServiceProvided',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('service', models.IntegerField(db_index=True, choices=[(1, '\u042d\u043a\u0441\u043f\u043e\u0440\u0442\u043d\u044b\u0435 \u043f\u043e\u0440\u0443\u0447\u0435\u043d\u0438\u044f')])),
            ],
            options={
                'verbose_name': '\u0423\u0441\u043b\u0443\u0433\u0430',
                'verbose_name_plural': '\u0423\u0441\u043b\u0443\u0433\u0438',
            },
        ),
        migrations.AlterModelOptions(
            name='team',
            options={'ordering': ('name',), 'verbose_name': '\u0420\u0430\u0431\u043e\u0447\u0430\u044f \u0433\u0440\u0443\u043f\u043f\u0430', 'verbose_name_plural': '\u0420\u0430\u0431\u043e\u0447\u0438\u0435 \u0433\u0440\u0443\u043f\u043f\u044b'},
        ),
        migrations.AlterModelOptions(
            name='terminal',
            options={'verbose_name': '\u0422\u0435\u0440\u043c\u0438\u043d\u0430\u043b', 'verbose_name_plural': '\u0422\u0435\u0440\u043c\u0438\u043d\u0430\u043b\u044b'},
        ),
        migrations.AlterModelOptions(
            name='vessel',
            options={'verbose_name': '\u0421\u0443\u0434\u043d\u043e', 'verbose_name_plural': '\u0421\u0443\u0434\u0430'},
        ),
        migrations.AlterModelOptions(
            name='voyage',
            options={'verbose_name': '\u0420\u0435\u0439\u0441', 'verbose_name_plural': '\u0420\u0435\u0439\u0441\u044b'},
        ),
        migrations.AddField(
            model_name='line',
            name='services',
            field=models.ManyToManyField(to='nutep.ServiceProvided'),
        ),
    ]
