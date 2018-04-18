# -*- coding: utf-8 -*-

from __future__ import division

import datetime
import json
import logging
from datetime import timedelta

import django_rq
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.core.cache import cache
from django.http import HttpResponse
from django.shortcuts import redirect, render
from django.utils.decorators import method_decorator
from django.utils.encoding import force_unicode
from django.utils.timezone import now
from django.views.generic.base import TemplateView
from django.views.generic.detail import SingleObjectMixin
from rest_framework import permissions, viewsets
from rest_framework.response import Response
from rest_framework.views import APIView

from nutep.forms import ReviseForm, TrackingForm
from nutep.models import (REVISE, TERMINAL_EXPORT, TRACKING, Company,
                          DateQueryEvent, News)
from nutep.serializers import (DateQueryReviseSerializer,                               
                               EmployeesSerializer, EventStatusSerializer,
                               NewsSerializer, UserSerializer)
from nutep.tasks import revise_task
from export.settings import BASE_RQ_PROC

logger = logging.getLogger('django.request')


class DeleteMixin(SingleObjectMixin):
    @method_decorator(login_required)
    def dispatch(self, *args, **kwargs):
        return super(DeleteMixin, self).dispatch(*args, **kwargs)

    def delete(self, request, *args, **kwargs):
        self.object = self.get_object()
        self.object.user = self.request.user
        self.object.deleted = True
        self.object.save()
        return HttpResponse(json.dumps({'pk': self.object.id}), content_type="application/json")


class BaseView(TemplateView):
    @method_decorator(login_required)
    def dispatch(self, *args, **kwargs):
        return super(BaseView, self).dispatch(*args, **kwargs)
    
    def news(self):        
        limit = 5
        return News.objects.all()[:limit]
    
    def get_company(self):
        return self.request.user.companies.filter(membership__is_general=True).first()

    def get_dealstats(self, dateformat="%d.%m.%Y %H:%M:%S"):
        company = self.get_company()
        if not company:
            return
        
    def get_context_data(self, **kwargs):
        context = super(BaseView, self).get_context_data(**kwargs)
        manager = self.request.user.managers.first()
        head = None
        if manager:
            manager.title = u"Ваш менеджер"            
            head = manager.head
            if head:
                head.title = u"Руководитель менеджера"
                                
        start_date = datetime.date.today().replace(day=1)
        revise_form = ReviseForm(user=self.request.user, initial={'start_date': start_date.strftime('%d.%m.%Y')})
        tracking_form = TrackingForm(user=self.request.user)
                
        context.update({
            'title': force_unicode('Рускон Онлайн'), 
            'manager': manager,
            'head': head,
            'news': self.news(),        
            'revise_form': revise_form,
            'tracking_form': tracking_form,
            'company': self.get_company()
        })         
        return context


def landing(request):    
    if request.user.is_authenticated():
        company = request.user.companies.filter(membership__is_general=True).first()        
        if company:
            return redirect(company.get_dashboard_url())                    
        return redirect(Company.DASHBOARD_VIEW)
    else:
        return redirect('login')


class BaseService(BaseView):
    TYPE = None
    def get_service(self):
        company = self.get_company()
        service = company.services.get(client_service__type=self.TYPE)
        return service
    def get_context_data(self, **kwargs):
        context = super(BaseService, self).get_context_data(**kwargs)        
        context.update({
            'service': self.get_service(),        
        })
        return context


class DashboardView(BaseView):
    template_name = 'dashboard.html'

    def get_context_data(self, **kwargs):
        context = super(DashboardView, self).get_context_data(**kwargs)
        context.update({
            'title': force_unicode('Рускон Онлайн'),        
        })
        return context


class ReviseView(BaseService):
    TYPE = REVISE
    template_name = 'revise.html'


class UserViewSet(viewsets.ModelViewSet):
    permission_classes = (permissions.IsAdminUser,)
    queryset = User.objects.all().order_by('-date_joined')
    serializer_class = UserSerializer
 
 
class ReviseViewSet(viewsets.ModelViewSet):
    serializer_class = DateQueryReviseSerializer
    def get_queryset(self):
        return DateQueryEvent.objects.for_user(self.request.user).filter(type=REVISE).order_by('-date')[:1]


class PingRevise(viewsets.ViewSet):
    def list(self, request):
        today = now()
        key = u'last_ping_revise_%s' % request.user.pk
        if cache.get(key):
            return Response({'job': 'cached'})
        cache.set(key, today, 300)   
        start_date = today - timedelta(days=360)
        end_date = today
        job = revise_task.delay(request.user, start_date, end_date)
        return Response({'job': job.id})  


class JobStatus(viewsets.ViewSet):
    def retrieve(self, request, pk):                
        queue = django_rq.get_queue(BASE_RQ_PROC)
        job = queue.fetch_job(pk)
        status = job.status if job else None
        return Response({'job': status})
    

class DealStats(viewsets.ViewSet):
    def list(self, request):       
        company = request.user.companies.filter(membership__is_general=True).first()
        if not company:
            return Response({})
        deal_stats = company.details.get('DealStats')
        if deal_stats:
            return Response({'deal_stats': deal_stats})
        return Response({})    
    

class EventViewSet(viewsets.ModelViewSet):    
    serializer_class = EventStatusSerializer
    def get_queryset(self):
        DateQueryEvent.objects.for_user(self.request.user).filter(status__in=(DateQueryEvent.ERROR, DateQueryEvent.PENDING)).order_by('-date')        
    

class EmployeesViewSet(viewsets.ModelViewSet):
    serializer_class = EmployeesSerializer
    def get_queryset(self):
        return self.request.user.managers.all()    


class NewsViewSet(viewsets.ModelViewSet):
    limit = 5
    serializer_class = NewsSerializer
    def get_queryset(self):        
        q = News.objects.all()
        return q[:self.limit]
