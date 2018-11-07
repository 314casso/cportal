# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from django.db import models

from django.contrib.contenttypes.fields import GenericRelation

from nutep.models import Company, DateQueryEvent, File


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
