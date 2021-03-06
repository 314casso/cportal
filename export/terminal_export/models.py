# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models

from nutep.base_models import BaseContainer
from nutep.models import DateQueryEvent, Nomenclature


class Container(BaseContainer):
    emptyweight = models.DecimalField(max_digits=10, decimal_places=3, blank=True, null=True)
    seal = models.CharField(max_length=150, blank=True, null=True)
    datein = models.DateField(blank=True, null=True)
    dateout = models.DateTimeField(blank=True, null=True)
    contract = models.CharField(max_length=150, blank=True, null=True)
    terminal = models.CharField(max_length=150, blank=True, null=True)
    

class Stuffing(models.Model):
    container = models.ForeignKey(Container, blank=True, null=True, related_name="stuffs")    
    staffdate = models.DateField(blank=True, null=True)
    vagon = models.CharField(max_length=50, blank=True, null=True)
    cargomark = models.CharField(max_length=50, blank=True, null=True)
    quantity = models.IntegerField(blank=True, null=True)
    grossweight = models.DecimalField(max_digits=10, decimal_places=3, blank=True, null=True)
    netweight = models.DecimalField(max_digits=10, decimal_places=3, blank=True, null=True)
    class Meta:
        ordering = ('id',)


class TerminalExport(models.Model):
    rowindex = models.IntegerField(blank=True, null=True)
    event = models.ForeignKey(DateQueryEvent, related_name="terminalexports")
    container = models.OneToOneField(Container, blank=True, null=True)
    nomenclature = models.ForeignKey(Nomenclature, blank=True, null=True)    
    class Meta:
        ordering = ('rowindex',)
		

class LineDemurrage(models.Model):    
    event = models.ForeignKey(DateQueryEvent, related_name="linedemurrages")
    container = models.OneToOneField(Container, blank=True, null=True)
    nomenclature = models.ForeignKey(Nomenclature, blank=True, null=True)       
    emptydate = models.DateTimeField(blank=True, null=True)
    status = models.CharField(max_length=50, blank=True, null=True)
    stuffdate = models.DateTimeField(blank=True, null=True) 
    freetime = models.IntegerField(blank=True, null=True) 
    deadline = models.DateTimeField(blank=True, null=True)
    overtime = models.IntegerField(blank=True, null=True)
    emptytime = models.IntegerField(blank=True, null=True)
    cargotime = models.IntegerField(blank=True, null=True)
    totaldays = models.IntegerField(blank=True, null=True)
    cargomark = models.CharField(max_length=50, blank=True, null=True)

    def __unicode__(self):
        return u'{0}'.format(self.container)        

    class Meta:
        ordering = ('overtime',)