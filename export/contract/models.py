# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from django.contrib.contenttypes.fields import GenericRelation
from django.contrib.postgres.fields.jsonb import JSONField
from django.db import models

from nutep.models import Company, DateQueryEvent, File


class ClientOrder(models.Model):
    name = models.CharField(max_length=50, db_index=True)
    guid = models.CharField(max_length=36)
    company = models.ForeignKey(Company, blank=True, null=True)
    date = models.DateTimeField(blank=True, db_index=True, null=True)
    contracts = models.ManyToManyField('Contract', related_name="orders")
    event = models.ForeignKey(DateQueryEvent, related_name="orderevents", blank=True, null=True)
    data = JSONField(blank=True, null=True)    
    data_event = models.ForeignKey(DateQueryEvent, related_name="orderdataevents", blank=True, null=True)
    files = GenericRelation(File)
    def __unicode__(self):
        return u'{0}'.format(self.name)


class Contract(models.Model):
    name = models.CharField(max_length=50, db_index=True)
    guid = models.CharField(max_length=36, unique=True)
    company = models.ForeignKey(Company, blank=True, null=True)
    def __unicode__(self):
        return u'{0}'.format(self.name)


class ContractEvent(models.Model):    
    contract = models.ForeignKey(Contract)
    event = models.OneToOneField(DateQueryEvent, related_name="contractevent")
    files = GenericRelation(File)
    def __unicode__(self):
        return u'{0}'.format(self.contract)
