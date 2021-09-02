# -*- coding: utf-8 -*-

import zipfile
from io import BytesIO

from django.http import JsonResponse
from rest_framework import viewsets
from rest_framework.response import Response

from django.http import HttpResponse

import nutep

from nutep.views import BaseService
from export.local_settings import WEB_SERVISES
from inspection.services import InspectionService
from inspection.models import Inspection
from inspection.serializers import InspectionSerializer

SERVICE_NAME = 'cp_dc'

class DashboardView(BaseService):
    TYPE = nutep.models.INSPECTION
    template_name = 'inspection.html'    
    
def get_inspections(request):
    company = request.user.companies.filter(membership__is_general=True).first()
    service = InspectionService(WEB_SERVISES[SERVICE_NAME])    
    return JsonResponse(service.get_inspections(request.user, company), safe=False)
        
def get_inspection(request, guid):
    company = request.user.companies.filter(membership__is_general=True).first()
    service = InspectionService(WEB_SERVISES[SERVICE_NAME])    
    service.get_inspection(request.user, company, guid)  
    return JsonResponse({'result': True})

def inspection_zip(request, pk):
    inspection = Inspection.objects.get(pk=pk)
    
    byte_data = BytesIO()
    zip_file = zipfile.ZipFile(byte_data, "w")

    for f in inspection.files.all():             
        zip_file.write(f.file.path, f.file.name)
    
    zip_file.close()

    response = HttpResponse(byte_data.getvalue(), content_type='application/zip')
    response['Content-Disposition'] = 'attachment; filename=%s-%s.zip' % (inspection.container.replace(" ", ""), inspection.date.strftime("%d%m%Y"))
    
    zip_file.printdir()
    return response
   

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
            service = InspectionService(WEB_SERVISES[SERVICE_NAME])    
            inspection = service.get_inspection(self.request.user, company, pk)  

        serializer = InspectionSerializer(inspection)
        return Response(serializer.data)
