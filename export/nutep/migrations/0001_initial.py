# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models
import nutep.models
import django.db.models.deletion
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        ('contenttypes', '0002_remove_content_type_name'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='BaseError',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('object_id', models.PositiveIntegerField()),
                ('date', models.DateTimeField(auto_now_add=True)),
                ('code', models.CharField(db_index=True, max_length=50, null=True, blank=True)),
                ('field', models.CharField(db_index=True, max_length=50, null=True, blank=True)),
                ('message', models.TextField()),
                ('type', models.IntegerField(default=3, blank=True, db_index=True, choices=[(1, '\u041e\u0448\u0438\u0431\u043a\u0430 \u0443\u0447\u0435\u0442\u043d\u043e\u0439 \u0441\u0438\u0441\u0442\u0435\u043c\u044b'), (4, '\u041e\u0448\u0438\u0431\u043a\u0430 \u043e\u0431\u043c\u0435\u043d\u0430 \u0434\u0430\u043d\u043d\u044b\u0445'), (2, '\u041e\u0448\u0438\u0431\u043a\u0430 \u0434\u0430\u043d\u043d\u044b\u0445'), (3, '\u041e\u0448\u0438\u0431\u043a\u0430')])),
                ('content_type', models.ForeignKey(to='contenttypes.ContentType')),
            ],
        ),
        migrations.CreateModel(
            name='Container',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(max_length=12, db_index=True)),
                ('SOC', models.BooleanField(default=False)),
                ('size', models.CharField(max_length=2, db_index=True)),
                ('type', models.CharField(max_length=3, db_index=True)),
                ('seal', models.CharField(max_length=150, null=True, blank=True)),
                ('cargo', models.CharField(max_length=255, null=True, blank=True)),
                ('netto', models.DecimalField(null=True, max_digits=8, decimal_places=3, blank=True)),
                ('gross', models.DecimalField(null=True, max_digits=8, decimal_places=3, blank=True)),
                ('tare', models.DecimalField(null=True, max_digits=8, decimal_places=3, blank=True)),
                ('package', models.CharField(max_length=150, null=True, blank=True)),
                ('quantity', models.PositiveIntegerField(null=True, blank=True)),
            ],
            options={
                'ordering': ('name',),
                'verbose_name': '\u041a\u043e\u043d\u0442\u0435\u0439\u043d\u0435\u0440',
                'verbose_name_plural': '\u041a\u043e\u043d\u0442\u0435\u0439\u043d\u0435\u0440\u044b',
            },
        ),
        migrations.CreateModel(
            name='Contract',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('deleted', models.BooleanField(default=False, verbose_name=b'\xd0\x9f\xd0\xbe\xd0\xbc\xd0\xb5\xd1\x82\xd0\xba\xd0\xb0 \xd1\x83\xd0\xb4\xd0\xb0\xd0\xbb\xd0\xb5\xd0\xbd\xd0\xb8\xd1\x8f')),
                ('name', models.CharField(max_length=150, verbose_name=b'\xd0\x9d\xd0\xb0\xd0\xb8\xd0\xbc\xd0\xb5\xd0\xbd\xd0\xbe\xd0\xb2\xd0\xb0\xd0\xbd\xd0\xb8\xd0\xb5', db_index=True)),
                ('guid', models.CharField(max_length=50, null=True, db_index=True)),
                ('startdate', models.DateTimeField(db_index=True)),
                ('expired', models.DateTimeField(db_index=True)),
            ],
            options={
                'ordering': ('name',),
                'verbose_name': '\u0414\u043e\u0433\u043e\u0432\u043e\u0440',
                'verbose_name_plural': '\u0414\u043e\u0433\u043e\u0432\u043e\u0440\u044b',
            },
        ),
        migrations.CreateModel(
            name='Draft',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(max_length=150, verbose_name=b'BL', db_index=True)),
                ('guid', models.CharField(max_length=50)),
                ('date', models.DateTimeField()),
                ('shipper', models.CharField(max_length=255, null=True, blank=True)),
                ('consignee', models.CharField(max_length=255, null=True, blank=True)),
                ('finalDestination', models.CharField(max_length=255, null=True, blank=True)),
                ('POD', models.CharField(max_length=150, null=True, blank=True)),
                ('POL', models.CharField(max_length=150, null=True, blank=True)),
                ('finstatus', models.BooleanField(default=False)),
                ('status', models.BooleanField(default=False)),
                ('poruchenie', models.BooleanField(default=False)),
                ('poruchenieNums', models.CharField(max_length=150, null=True, blank=True)),
                ('notify', models.CharField(max_length=255, null=True, blank=True)),
            ],
            options={
                'ordering': ('name',),
                'verbose_name': '\u041a\u043e\u043d\u043e\u0441\u0430\u043c\u0435\u043d\u0442',
                'verbose_name_plural': '\u041a\u043e\u043d\u043e\u0441\u0430\u043c\u0435\u043d\u0442\u044b',
            },
        ),
        migrations.CreateModel(
            name='HistoryMeta',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('object_id', models.PositiveIntegerField()),
                ('is_created', models.BooleanField(default=False)),
                ('date', models.DateTimeField(db_index=True, null=True, blank=True)),
                ('content_type', models.ForeignKey(to='contenttypes.ContentType')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, blank=True, to=settings.AUTH_USER_MODEL, null=True)),
            ],
        ),
        migrations.CreateModel(
            name='Line',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('deleted', models.BooleanField(default=False, verbose_name=b'\xd0\x9f\xd0\xbe\xd0\xbc\xd0\xb5\xd1\x82\xd0\xba\xd0\xb0 \xd1\x83\xd0\xb4\xd0\xb0\xd0\xbb\xd0\xb5\xd0\xbd\xd0\xb8\xd1\x8f')),
                ('name', models.CharField(max_length=150, verbose_name=b'\xd0\x9d\xd0\xb0\xd0\xb8\xd0\xbc\xd0\xb5\xd0\xbd\xd0\xbe\xd0\xb2\xd0\xb0\xd0\xbd\xd0\xb8\xd0\xb5', db_index=True)),
                ('guid', models.CharField(max_length=50, null=True, db_index=True)),
            ],
            options={
                'ordering': ('name',),
                'verbose_name': '\u041b\u0438\u043d\u0438\u044f',
                'verbose_name_plural': '\u041b\u0438\u043d\u0438\u0438',
            },
        ),
        migrations.CreateModel(
            name='Readiness',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('size', models.CharField(max_length=2, db_index=True)),
                ('type', models.CharField(max_length=3, db_index=True)),
                ('ordered', models.PositiveIntegerField(null=True, blank=True)),
                ('done', models.PositiveIntegerField(null=True, blank=True)),
                ('draft', models.ForeignKey(related_name='readiness', to='nutep.Draft')),
            ],
            options={
                'ordering': ('id',),
                'verbose_name': '\u0413\u043e\u0442\u043e\u0432\u043d\u043e\u0441\u0442\u044c',
                'verbose_name_plural': '\u0413\u043e\u0442\u043e\u0432\u043d\u043e\u0441\u0442\u044c',
            },
        ),
        migrations.CreateModel(
            name='Terminal',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('deleted', models.BooleanField(default=False, verbose_name=b'\xd0\x9f\xd0\xbe\xd0\xbc\xd0\xb5\xd1\x82\xd0\xba\xd0\xb0 \xd1\x83\xd0\xb4\xd0\xb0\xd0\xbb\xd0\xb5\xd0\xbd\xd0\xb8\xd1\x8f')),
                ('name', models.CharField(max_length=150, verbose_name=b'\xd0\x9d\xd0\xb0\xd0\xb8\xd0\xbc\xd0\xb5\xd0\xbd\xd0\xbe\xd0\xb2\xd0\xb0\xd0\xbd\xd0\xb8\xd0\xb5', db_index=True)),
                ('guid', models.CharField(max_length=50, null=True, db_index=True)),
            ],
            options={
                'ordering': ('name',),
                'verbose_name': '\u0422\u0435\u0440\u043c\u0438\u043d\u0430\u043b',
                'verbose_name_plural': '\u0422\u0435\u0440\u043c\u0438\u043d\u0430\u043b\u044b',
            },
        ),
        migrations.CreateModel(
            name='UploadedTemplate',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('deleted', models.BooleanField(default=False, verbose_name=b'\xd0\x9f\xd0\xbe\xd0\xbc\xd0\xb5\xd1\x82\xd0\xba\xd0\xb0 \xd1\x83\xd0\xb4\xd0\xb0\xd0\xbb\xd0\xb5\xd0\xbd\xd0\xb8\xd1\x8f')),
                ('attachment', models.FileField(upload_to=nutep.models.attachment_path, verbose_name=b'\xd0\xa4\xd0\xb0\xd0\xb9\xd0\xbb \xd1\x88\xd0\xb0\xd0\xb1\xd0\xbb\xd0\xbe\xd0\xbd\xd0\xb0')),
                ('status', models.IntegerField(default=1, blank=True, db_index=True, choices=[(1, '\u041d\u043e\u0432\u044b\u0439'), (2, '\u0412 \u043e\u0431\u0440\u0430\u0431\u043e\u0442\u043a\u0435'), (3, '\u041e\u0431\u0440\u0430\u0431\u043e\u0442\u0430\u043d'), (500, '\u041e\u0448\u0438\u0431\u043a\u0430')])),
                ('http_code', models.CharField(max_length=50, null=True, verbose_name=b'HTTP \xd0\x9a\xd0\xbe\xd0\xb4', blank=True)),
                ('xml_response', models.TextField(null=True, verbose_name=b'XML \xd0\xbe\xd1\x82\xd0\xb2\xd0\xb5\xd1\x82', blank=True)),
                ('contract', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, blank=True, to='nutep.Contract', null=True)),
            ],
            options={
                'ordering': ('-id',),
                'verbose_name': '\u0428\u0430\u0431\u043b\u043e\u043d',
                'verbose_name_plural': '\u0428\u0430\u0431\u043b\u043e\u043d\u044b',
            },
        ),
        migrations.CreateModel(
            name='UserProfile',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('guid', models.CharField(max_length=50, null=True)),
                ('lines', models.ManyToManyField(to='nutep.Line')),
                ('user', models.ForeignKey(related_name='profile', to=settings.AUTH_USER_MODEL, unique=True)),
            ],
        ),
        migrations.CreateModel(
            name='Vessel',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('deleted', models.BooleanField(default=False, verbose_name=b'\xd0\x9f\xd0\xbe\xd0\xbc\xd0\xb5\xd1\x82\xd0\xba\xd0\xb0 \xd1\x83\xd0\xb4\xd0\xb0\xd0\xbb\xd0\xb5\xd0\xbd\xd0\xb8\xd1\x8f')),
                ('name', models.CharField(max_length=150, verbose_name=b'\xd0\x9d\xd0\xb0\xd0\xb8\xd0\xbc\xd0\xb5\xd0\xbd\xd0\xbe\xd0\xb2\xd0\xb0\xd0\xbd\xd0\xb8\xd0\xb5', db_index=True)),
                ('guid', models.CharField(max_length=50, null=True, db_index=True)),
            ],
            options={
                'ordering': ('name',),
                'verbose_name': '\u0421\u0443\u0434\u043d\u043e',
                'verbose_name_plural': '\u0421\u0443\u0434\u0430',
            },
        ),
        migrations.CreateModel(
            name='Voyage',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('deleted', models.BooleanField(default=False, verbose_name=b'\xd0\x9f\xd0\xbe\xd0\xbc\xd0\xb5\xd1\x82\xd0\xba\xd0\xb0 \xd1\x83\xd0\xb4\xd0\xb0\xd0\xbb\xd0\xb5\xd0\xbd\xd0\xb8\xd1\x8f')),
                ('name', models.CharField(max_length=150, verbose_name=b'\xd0\x9d\xd0\xb0\xd0\xb8\xd0\xbc\xd0\xb5\xd0\xbd\xd0\xbe\xd0\xb2\xd0\xb0\xd0\xbd\xd0\xb8\xd0\xb5', db_index=True)),
                ('guid', models.CharField(max_length=50, null=True, db_index=True)),
                ('flag', models.CharField(max_length=100, null=True, blank=True)),
                ('etd', models.DateTimeField(null=True, blank=True)),
                ('vessel', models.ForeignKey(related_name='voyages', to='nutep.Vessel', null=True)),
            ],
            options={
                'ordering': ('name',),
                'verbose_name': '\u0420\u0435\u0439\u0441',
                'verbose_name_plural': '\u0420\u0435\u0439\u0441\u044b',
            },
        ),
        migrations.AddField(
            model_name='uploadedtemplate',
            name='voyage',
            field=models.ForeignKey(related_name='templates', on_delete=django.db.models.deletion.PROTECT, blank=True, to='nutep.Voyage', null=True),
        ),
        migrations.AddField(
            model_name='draft',
            name='line',
            field=models.ForeignKey(to='nutep.Line'),
        ),
        migrations.AddField(
            model_name='draft',
            name='template',
            field=models.ForeignKey(related_name='drafts', to='nutep.UploadedTemplate'),
        ),
        migrations.AddField(
            model_name='draft',
            name='user',
            field=models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, blank=True, to=settings.AUTH_USER_MODEL, null=True),
        ),
        migrations.AddField(
            model_name='draft',
            name='voyage',
            field=models.ForeignKey(related_name='drafts', to='nutep.Voyage', null=True),
        ),
        migrations.AddField(
            model_name='contract',
            name='line',
            field=models.ForeignKey(related_name='contracts', to='nutep.Line'),
        ),
        migrations.AddField(
            model_name='contract',
            name='terminal',
            field=models.ForeignKey(to='nutep.Terminal'),
        ),
        migrations.AddField(
            model_name='container',
            name='draft',
            field=models.ForeignKey(related_name='containers', to='nutep.Draft'),
        ),
        migrations.AddField(
            model_name='container',
            name='line',
            field=models.ForeignKey(blank=True, to='nutep.Line', null=True),
        ),
    ]
