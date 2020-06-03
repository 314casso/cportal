# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.utils.translation import ugettext_lazy as _
from django.contrib.contenttypes.fields import  GenericRelation
from django.db import models
from nutep.models import File, Company, DateQueryEvent


class Inspection(models.Model):
    container = models.CharField(_('container'), max_length=12)  
    guid = models.CharField(_('guid'), max_length=50)  
    date = models.DateTimeField(_('date'))  
    number = models.CharField(_('number'), max_length=20)            
    company = models.ForeignKey(Company, blank=True, null=True)
    event = models.ForeignKey(DateQueryEvent, blank=True, null=True)
    files = GenericRelation(File)
    
    def __unicode__(self):
        return self.container
        