# -*- coding: utf-8 -*-
# Generated by Django 1.11.10 on 2018-04-04 14:15
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('nutep', '0029_auto_20180220_1430'),
    ]

    operations = [
        migrations.CreateModel(
            name='ClientService',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=12)),
            ],
        ),
        migrations.CreateModel(
            name='CompanyService',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('is_active', models.BooleanField(default=False)),
                ('client_service', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='services', to='nutep.ClientService')),
                ('company', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='nutep.Company')),
            ],
        ),
        migrations.AddField(
            model_name='company',
            name='client_services',
            field=models.ManyToManyField(blank=True, related_name='companies', through='nutep.CompanyService', to='nutep.ClientService'),
        ),
    ]