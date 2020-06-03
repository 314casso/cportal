# -*- coding: utf-8 -*-

import calendar
import datetime

from django.core.cache import cache
from django.http import JsonResponse
from rest_framework import viewsets

import nutep
from nutep.serializers import DateQueryReviseSerializer
from nutep.views import BaseService
from export.local_settings import WEB_SERVISES
from inspection.services import InspectionService
from inspection.models import Inspection
from django.shortcuts import get_object_or_404
from rest_framework.response import Response
from inspection.serializers import InspectionSerializer


class DashboardView(BaseService):
    TYPE = nutep.models.INSPECTION
    template_name = 'inspection.html'    
    
def get_inspections(request):
    company = request.user.companies.filter(membership__is_general=True).first()
    service = InspectionService(WEB_SERVISES['cp'])    
    return JsonResponse(service.get_inspections(request.user, company), safe=False)
        
def get_inspection(request, guid):
    company = request.user.companies.filter(membership__is_general=True).first()
    service = InspectionService(WEB_SERVISES['cp'])    
    service.get_inspection(request.user, company, guid)  
    return JsonResponse({'result': True})

class InspectionViewSet(viewsets.ViewSet):     
    def list(self, request):
        queryset = Inspection.objects.all()
        serializer = InspectionSerializer(queryset, many=True)
        return Response(serializer.data)
    def retrieve(self, request, pk=None):     
        try:            
            inspection = Inspection.objects.get(guid=pk)
        except Inspection.DoesNotExist:
            company = self.request.user.companies.filter(membership__is_general=True).first()
            service = InspectionService(WEB_SERVISES['cp'])    
            inspection = service.get_inspection(self.request.user, company, pk)  

        serializer = InspectionSerializer(inspection)
        return Response(serializer.data)
