# -*- coding: utf-8 -*-

import calendar
import datetime

from django.core.cache import cache
from django.http import JsonResponse
from rest_framework import viewsets

from contpics.tasks import contpics_task

import nutep
from nutep.serializers import DateQueryReviseSerializer
from nutep.views import BaseService


class DashboardView(BaseService):
    TYPE = nutep.models.CONTPICS
    template_name = 'contpics.html'    
    

def ping_contpics(request, start_date):
    company = request.user.companies.filter(membership__is_general=True).first()
    today = datetime.datetime.now()
    start_date = datetime.datetime.strptime(start_date, "%d%m%Y").date().replace(day=1)
    end_date = start_date.replace(day=calendar.monthrange(start_date.year, start_date.month)[1]) 
    key = u'get_service_contpics_%s_%s' % (request.user.pk, start_date)
    if cache.get(key):
        return JsonResponse({'job': 'cached'})
    cache.set(key, today, 3600*12)     
    job = contpics_task.delay(request.user, company, start_date, end_date)    
    return JsonResponse({'job': job.id})


class ContPicsViewSet(viewsets.ModelViewSet):     
    serializer_class = DateQueryReviseSerializer
    def get_queryset(self):
        q = nutep.models.DateQueryEvent.objects.for_user(
            self.request.user).filter(type=nutep.models.CONTPICS)
        q = q.exclude(status__in=(nutep.models.DateQueryEvent.PENDING, nutep.models.DateQueryEvent.ERROR))
        return q.order_by('-date')[:20]
