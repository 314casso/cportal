# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models

from nutep.base_models import BaseContainer
from nutep.models import DateQueryEvent


class Container(BaseContainer):
    pass


class Platform(models.Model):
    number = models.CharField(max_length=50)
    foot = models.IntegerField(blank=True, null=True)
    length = models.DecimalField(max_digits=10, decimal_places=3, blank=True, null=True)
    model = models.CharField(max_length=50, blank=True, null=True)
    mtu = models.CharField(max_length=50, blank=True, null=True)


class RailData(models.Model):
    train = models.CharField(max_length=50, blank=True, null=True)
    invoice = models.CharField(max_length=50, blank=True, null=True)
    departurestation = models.CharField(max_length=50, blank=True, null=True)
    departuredate = models.DateField(blank=True, null=True)
    destinationstation = models.CharField(max_length=50, blank=True, null=True)
    totaldistance = models.IntegerField(blank=True, null=True)
    estimatedtime = models.IntegerField(blank=True, null=True)


class RailTracking(models.Model):    
    operationstation = models.CharField(max_length=50, blank=True, null=True)
    daysinroute = models.IntegerField(blank=True, null=True)
    remainingdistance = models.IntegerField(blank=True, null=True)
    arrivaldate = models.DateField(blank=True, null=True)


class FreightData(models.Model):
    bl = models.CharField(max_length=50, blank=True, null=True)
    deal = models.CharField(max_length=50, blank=True, null=True)
    vessel = models.CharField(max_length=50, blank=True, null=True)
    voyage = models.CharField(max_length=50, blank=True, null=True)
    dateoutplan = models.DateField(blank=True, null=True)
    pod = models.CharField(max_length=50, blank=True, null=True)
    podcountry = models.CharField(max_length=50, blank=True, null=True)


class FreightTracking(models.Model):
    departuredate = models.DateField(blank=True, null=True)
    arrivaldate = models.DateField(blank=True, null=True)
    pot = models.CharField(max_length=50, blank=True, null=True)
    arrivaldatepot = models.DateField(blank=True, null=True)
    departuredatepot = models.DateField(blank=True, null=True)
    daysinroute = models.IntegerField(blank=True, null=True)
    arrivaldateactual = models.DateField(blank=True, null=True)
    

class RailFreightTracking(models.Model):
    event = models.ForeignKey(DateQueryEvent, related_name="tracks")
    container = models.ForeignKey(Container, blank=True, null=True)
    platform = models.ForeignKey(Platform, blank=True, null=True)
    raildata = models.ForeignKey(RailData, blank=True, null=True)
    railtracking = models.ForeignKey(RailTracking, blank=True, null=True)
    freightdata = models.ForeignKey(FreightData, blank=True, null=True)
    freighttracking = models.ForeignKey(FreightTracking, blank=True, null=True)
