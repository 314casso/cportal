# -*- coding: utf-8 -*-

from __future__ import division

import json
import logging

import suds
from django.contrib.auth.decorators import login_required
from django.core.files.base import ContentFile
from django.core.paginator import EmptyPage, PageNotAnInteger, Paginator
from django.core.urlresolvers import reverse
from django.http import HttpResponse, HttpResponseRedirect, JsonResponse
from django.shortcuts import redirect, render
from django.utils.decorators import method_decorator
from django.utils.encoding import force_text, force_unicode
from django.views.decorators.http import require_http_methods
from django.views.generic.base import TemplateView
from django.views.generic.detail import SingleObjectMixin
from django.views.generic.edit import DeleteView
from django_rq.decorators import job

from export.local_settings import WEB_SERVISES
from nutep.models import BaseError, News, File
import hashlib
from nutep.services import CRMService, PortalService, DealService, ReviseService,\
    TrackingService
import requests
import datetime
from nutep.forms import ReviseForm, TrackingForm
from django.contrib.contenttypes.models import ContentType
from django.contrib.auth.models import User
from rest_framework import viewsets
from nutep.serializers import UserSerializer


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
    
    def get_dealstats(self, dateformat="%d.%m.%Y %H:%M:%S"):
        if self.request.user.profile:
            deal_stats = self.request.user.profile.details.get('DealStats')
            if deal_stats:
                result = {}
                result['dealdate'] = datetime.datetime.strptime(deal_stats.get('FirstDeal'), dateformat)
                result['totaldeals'] = deal_stats.get('TotalDeals')
                result['lastmonth'] = deal_stats.get('LastMonth')
                result['days_together'] = (datetime.datetime.now() - result['dealdate']).days
                return result

    def get_context_data(self, **kwargs):
        context = super(BaseView, self).get_context_data(**kwargs)
        manager = self.request.user.managers.first()
        head = None
        if manager:
            manager.title = u"Ваш менеджер"            
            head = manager.head
            if head:
                head.title = u"Руководитель менеджера"
        
        dealstats = self.get_dealstats()
        
        start_date = datetime.date.today().replace(day=1)
        revise_form = ReviseForm(user=self.request.user, initial={'start_date': start_date.strftime('%d.%m.%Y')})
        tracking_form = TrackingForm(user=self.request.user)
                
        context.update({
            'title': force_unicode('Рускон Онлайн'), 
            'manager': manager,
            'head': head,
            'news': self.news(),
            'dealstats': dealstats,
            'revise_form': revise_form,
            'tracking_form': tracking_form,
        })         
        return context


@login_required
def get_last_revises(request):    
    ct = ContentType.objects.get_for_model(request.user)
    values = set(User.objects.filter(profile__payers__in=request.user.profile.payers.all()).values_list('id', flat=True)) 
    revises = File.objects.filter(content_type__pk=ct.id, object_id__in=values).order_by("-date")[:5]   
    return JsonResponse([obj.as_dict() for obj in revises], safe=False)    


@require_http_methods(["POST"])
@login_required
def get_revise(request):
    if request.method == 'POST':
        form = ReviseForm(request.POST)
        if form.is_valid():
            user = form.cleaned_data['profile'].user
            start_date = form.cleaned_data['start_date']
            end_date = form.cleaned_data['end_date']
        try:        
            revise_service = ReviseService(WEB_SERVISES['erp'])                        
            response = revise_service.get_revise(user, start_date, end_date)
            status = True if response else False                       
            return HttpResponse(json.dumps({ 'status':status, 'message': u'Файл ведомости успешно получен', 'title': u'Загрузка' }), content_type="application/json")
        except Exception as e:
            return HttpResponse(force_text(e), status=400) 
        

@require_http_methods(["POST"])
@login_required
def get_tracking(request):
    if request.method == 'POST':
        form = TrackingForm(request.POST)
        if form.is_valid():
            user = form.cleaned_data['profile'].user            
        try:        
            tracking_service = TrackingService(WEB_SERVISES['report'])                        
            response = tracking_service.get_track(user)
            status = True if response else False                       
            return HttpResponse(json.dumps({ 'status':status, 'message': u'Файл слежения успешно получен', 'title': u'Загрузка' }), content_type="application/json")
        except Exception as e:
            return HttpResponse(force_text(e), status=400)
        

def landing(request):
    if request.user.is_authenticated():
        return redirect('services')
    context = {
        'title': force_unicode('Рускон'),
    }
    return render(request, 'landing.html', context)


class ServiceView(BaseView):
    template_name = 'base.html'

    def get_context_data(self, **kwargs):
        context = super(ServiceView, self).get_context_data(**kwargs)
        context.update({
            'title': force_unicode('Рускон Онлайн'),        
        })
        return context


class UserViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows users to be viewed or edited.
    """
    queryset = User.objects.all().order_by('-date_joined')
    serializer_class = UserSerializer

 
