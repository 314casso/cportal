# -*- coding: utf-8 -*-
import datetime

from django.core.cache import cache
from django.db.models import Q
from django.http import JsonResponse
from django.shortcuts import render
from django.utils.timezone import now
from rest_framework import viewsets
from rest_framework.pagination import PageNumberPagination

import nutep
from contract.models import ClientOrder, Contract
from contract.serializers import (ContractSerializer,
                                  DateQueryContractSerializer,
                                  DateQueryOrderDataSerializer,
                                  DateQueryOrderSerializer)
from contract.tasks import (contract_files_task, contract_task,
                            order_data_task, order_list_task)
from nutep.models import CONTRACT_FILES, ORDER_LIST, DateQueryEvent
from nutep.views import BaseService


def ping_contacts(request):
    company = request.user.companies.filter(membership__is_general=True).first()       
    job = contract_task.delay(request.user, company)    
    return JsonResponse({'job': job.id})


def ping_orders(request):
    today = now()
    key = u'last_ping_orders_%s' % request.user.pk
    if cache.get(key):
        return JsonResponse({'job': 'cached'})
    cache.set(key, today, 300)   
    company = request.user.companies.filter(membership__is_general=True).first()       
    job = order_list_task.delay(request.user, company, '3158c5cb-5e31-11e3-a3f9-000c29c1ffac')    
    return JsonResponse({'job': job.id})  


def ping_order_data(request, pk):
    client_order = ClientOrder.objects.get(pk=pk)
    company = request.user.companies.filter(membership__is_general=True).first()       
    job = order_data_task.delay(request.user, company, client_order)    
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


class OrderListDashboardView(BaseService):
    TYPE = nutep.models.ORDER_LIST
    template_name = 'orderlist.html' 


class StandardResultsSetPagination(PageNumberPagination):
    page_size = 7
    page_size_query_param = 'page_size'
    max_page_size = 1000


class OrderViewSet(viewsets.ModelViewSet):    
    serializer_class = DateQueryOrderDataSerializer
    pagination_class = StandardResultsSetPagination
    def get_queryset(self):                
        event = DateQueryEvent.objects.for_user(self.request.user).filter(status=DateQueryEvent.SUCCESS, type=ORDER_LIST).order_by('-date').first()
        if not event:
            return ClientOrder.objects.none()
        orderevents = event.orderevents.all()
        contract = self.request.query_params.get('contract', None)
        name = self.request.query_params.get('name', None)        
        platform = self.request.query_params.get('platform', None)
        perepodacha = self.request.query_params.get('perepodacha', None)
        if name:            
            orderevents = orderevents.filter(name__contains=name).distinct()        
        if contract:
            orderevents = orderevents.filter(contracts__name__contains=contract).distinct()                
        if platform:            
            like_arg = "%%%s%%" % platform            
            orderevents = orderevents.extra(where=["data ->> %s LIKE %s"], params=['platforms', like_arg])
        if perepodacha:
            like_arg = "%%%s%%" % perepodacha            
            orderevents = orderevents.extra(where=["data ->> %s LIKE %s"], params=['perepodacha', like_arg])
                    
        return orderevents.order_by('-date')


class OrderDataViewSet(viewsets.ModelViewSet):
    serializer_class = DateQueryOrderDataSerializer
    def get_queryset(self):        
        client_order = self.request.query_params.get('pk', None)        
        return ClientOrder.objects.filter(pk=client_order)        
