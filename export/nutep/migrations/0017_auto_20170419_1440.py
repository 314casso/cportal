# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('nutep', '0016_mission_draft'),
    ]

    operations = [
        migrations.CreateModel(
            name='Order',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('deleted', models.BooleanField(default=False, verbose_name=b'\xd0\x9f\xd0\xbe\xd0\xbc\xd0\xb5\xd1\x82\xd0\xba\xd0\xb0 \xd1\x83\xd0\xb4\xd0\xb0\xd0\xbb\xd0\xb5\xd0\xbd\xd0\xb8\xd1\x8f')),
                ('contract', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, blank=True, to='nutep.Contract', null=True)),
                ('owner', models.ForeignKey(blank=True, to=settings.AUTH_USER_MODEL, null=True)),
                ('teams', models.ManyToManyField(to='nutep.Team', blank=True)),
                ('voyage', models.ForeignKey(related_name='orders', on_delete=django.db.models.deletion.PROTECT, blank=True, to='nutep.Voyage', null=True)),
            ],
        ),
        migrations.RemoveField(
            model_name='draft',
            name='template',
        ),
        migrations.RemoveField(
            model_name='uploadedtemplate',
            name='contract',
        ),
        migrations.RemoveField(
            model_name='uploadedtemplate',
            name='voyage',
        ),
        migrations.AlterField(
            model_name='serviceprovided',
            name='service',
            field=models.CharField(db_index=True, unique=True, max_length=5, choices=[(b'00001', '\u042d\u043a\u0441\u043f\u043e\u0440\u0442\u043d\u044b\u0435 \u043f\u043e\u0440\u0443\u0447\u0435\u043d\u0438\u044f'), (b'00002', '\u041f\u0440\u043e\u0447\u0438\u0435 \u0434\u043e\u043a\u0443\u043c\u0435\u043d\u0442\u044b')]),
        ),
        migrations.AddField(
            model_name='draft',
            name='order',
            field=models.ForeignKey(related_name='drafts', blank=True, to='nutep.Order', null=True),
        ),
        migrations.AddField(
            model_name='uploadedtemplate',
            name='order',
            field=models.ForeignKey(blank=True, to='nutep.Order', null=True),
        ),
        migrations.AlterUniqueTogether(
            name='order',
            unique_together=set([('voyage', 'contract')]),
        ),
    ]
