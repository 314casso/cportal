# -*- coding: utf-8 -*-
import datetime

from django.core.cache import cache
from django.http import JsonResponse
from django.shortcuts import render
from rest_framework import viewsets

import nutep
from contract.models import Contract
from contract.serializers import ContractSerializer, \
    DateQueryContractSerializer
from contract.tasks import contract_files_task, contract_task
from nutep.models import CONTRACT_FILES, DateQueryEvent
from nutep.views import BaseService


def ping_contacts(request):
    company = request.user.companies.filter(membership__is_general=True).first()       
    job = contract_task.delay(request.user, company)    
    return JsonResponse({'job': job.id})


def ping_files(request, pk):
    company = request.user.companies.filter(membership__is_general=True).first()       
    contract = Contract.objects.get(pk=pk)
    job = contract_files_task.delay(request.user, company, contract)    
    return JsonResponse({'job': job.id})


class ContractViewSet(viewsets.ModelViewSet):    
    serializer_class = ContractSerializer
    def get_queryset(self):
        company = self.request.user.companies.filter(membership__is_general=True).first()           
        return Contract.objects.filter(company=company).order_by('name')


class ContractFileViewSet(viewsets.ModelViewSet):    
    serializer_class = DateQueryContractSerializer
    def get_queryset(self):
        contract = self.request.query_params.get('contract', None)        
        q = DateQueryEvent.objects.for_user(self.request.user).filter(type=CONTRACT_FILES, contractevent__contract_id=contract)
        q = q.exclude(status__in=(nutep.models.DateQueryEvent.PENDING, nutep.models.DateQueryEvent.ERROR))
        return q.order_by('-date')[:1]


class DashboardView(BaseService):
    TYPE = nutep.models.CONTRACT_FILES
    template_name = 'contract.html'   