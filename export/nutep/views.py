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
from nutep.forms import TemplateForm
from nutep.models import (BaseError, Contract, Draft, UploadedTemplate, Vessel,
                          Voyage, Order, Mission)
from nutep.services import DraftService, ExcelHelper, LoadingListService,\
    MissionService
import hashlib

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


class TemplateDeleteView(DeleteMixin, DeleteView):
    model = UploadedTemplate


@login_required
def template_detail(request, pk):
    template = UploadedTemplate.objects.get(pk=pk)
    context = {
        'template_detail.html': template,
    }
    return render(request, 'base.html', context)


class BaseView(TemplateView):
    @method_decorator(login_required)
    def dispatch(self, *args, **kwargs):
        return super(BaseView, self).dispatch(*args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super(BaseView, self).get_context_data(**kwargs)
        orders = Order.objects.for_user(self.request.user).distinct().order_by('voyage__vessel__name', 'voyage__name', 'contract__line__name')       
        context.update({
            'title': force_unicode('Рускон Онлайн'),
            'orders': orders,
        })
        return context


class ServiceView(BaseView):
    template_name = 'base.html'

    def get_context_data(self, **kwargs):
        context = super(ServiceView, self).get_context_data(**kwargs)
        PER_PAGE = 10
        template_list = UploadedTemplate.objects.all()

        page = self.request.GET.get('page', 1)
        paginator = Paginator(template_list, PER_PAGE)
        try:
            templates = paginator.page(page)
        except PageNotAnInteger:
            templates = paginator.page(1)
        except EmptyPage:
            templates = paginator.page(paginator.num_pages)

        template_form = TemplateForm(user=self.request.user)
        template_form.fields['contract'].queryset = Contract.objects.for_user(
            self.request.user)
        template_form.title = force_text('Загрузка шаблона заявки')
        template_form.key = 'templateupload'
        context.update({
            'title': force_unicode('Рускон Онлайн'),
            'templates': templates,
            'template_form': template_form,
            'paginator': paginator,
            'page_obj': templates,
            'is_paginated': templates.has_other_pages(),
            'object_list': templates.object_list,
        })
        return context


@require_http_methods(["POST"])
@login_required
def get_loading_list(request, pk):
    if request.method == 'POST':
        try:
            ll_service = LoadingListService(WEB_SERVISES['draft'])            
            response = ll_service.get_loading_list(pk, request.user)            
            status = True if response else False                        
            return HttpResponse(json.dumps({'status': status, 'url': response.file.url }), content_type="application/json")
        except Exception as e:
            return HttpResponse(force_text(e), status=400)
        
        
@require_http_methods(["POST"])
@login_required
def get_mission_xlsx(request, pk):
    if request.method == 'POST':
        try:
            mission_service = MissionService(WEB_SERVISES['draft'])            
            response = mission_service.get_mission_xlsx(pk, request.user)            
            status = True if response else False                        
            return HttpResponse(json.dumps({'status': status, 'url': response.file.url }), content_type="application/json")
        except Exception as e:
            return HttpResponse(force_text(e), status=400)        


@login_required
def get_active_templates(request):
    active_templates = UploadedTemplate.objects.for_user(request.user).filter(
        status__in=(UploadedTemplate.ERROR, UploadedTemplate.INPROCESS,
                    UploadedTemplate.REFRESH)).distinct()[:10]
    return JsonResponse([obj.as_dict() for obj in active_templates], safe=False)


@login_required
def get_last_orders(request):
    last_orders = Order.objects.for_user(request.user).all().distinct().order_by('-id')[:10]
    return JsonResponse([order.as_dict() for order in last_orders], safe=False)


class TemplateDetailView(BaseView):
    template_name = 'template_details.html'

    def get_context_data(self, **kwargs):
        pk = kwargs.get('pk')
        template = UploadedTemplate.objects.get(pk=pk)
        context = super(TemplateDetailView, self).get_context_data(**kwargs)
        draft_queryset = Draft.objects.filter(order=template.order)
        missions = Mission.objects.filter(draft__order=template.order).exclude(files__isnull=True)
        total = len(draft_queryset)
        rediness = 0        
        if total:            
            rediness = int(len(draft_queryset.filter(poruchenie=True)) / total * 100)
        
        context.update({
            'title': force_unicode('Рускон Онлайн'),
            'template': template,
            'rediness': rediness,
            'missions': missions,
        })
        return context


class DraftListView(BaseView):
    template_name = 'drafts_list.html'
    def get_context_data(self, **kwargs):
        PER_PAGE = 100
        order_id = kwargs.get('order')
        order = Order.objects.get(pk=order_id)
        draft_queryset = Draft.objects.filter(order=order)
        
        missions = Mission.objects.filter(draft__order=order).exclude(files__isnull=True)
                
        total = len(draft_queryset)        
        rediness = 0        
        if total:            
            rediness = int(len(draft_queryset.filter(poruchenie=True)) / total * 100)            

        page = self.request.GET.get('page', 1)
        paginator = Paginator(draft_queryset, PER_PAGE)
        try:
            drafts = paginator.page(page)
        except PageNotAnInteger:
            drafts = paginator.page(1)
        except EmptyPage:
            drafts = paginator.page(paginator.num_pages)

        context = super(DraftListView, self).get_context_data(**kwargs)
        context.update({
            'title': force_unicode('Рускон Онлайн'),            
            'paginator': paginator,
            'page_obj': drafts,
            'is_paginated': drafts.has_other_pages(),
            'object_list': drafts.object_list,
            'voyage': order.voyage,
            'rediness': rediness,
            'order': order,
            'missions': missions,
        })
        return context


class DraftDetailView(BaseView):
    template_name = 'draft_details.html'

    def get_context_data(self, **kwargs):
        pk = kwargs.get('pk')
        draft = Draft.objects.get(pk=pk)
        context = super(DraftDetailView, self).get_context_data(**kwargs)
        context.update({
            'title': force_unicode('Рускон Онлайн'),
            'draft': draft,
        })
        return context


def landing(request):
    if request.user.is_authenticated():
        return redirect('services')
    context = {
        'title': force_unicode('Рускон'),
    }
    return render(request, 'landing.html', context)


@login_required
def delete_template(request, template_id):
    if request.method == 'POST':
        try:
            template = UploadedTemplate.objects.get(pk=template_id)
            template.deleted = True
            template.user = request.user
            template.save()
        except UploadedTemplate.DoesNotExist:
            return HttpResponse(u'Template id %s не найден' % template_id, status=404)


@require_http_methods(["POST"])
@login_required
def get_template_status(request, pk):
    if request.method == 'POST':
        try:
            draft_service = DraftService(WEB_SERVISES['draft'])            
            response = draft_service.update_status(pk, request.user)
            status = True if response else False
            return HttpResponse(json.dumps({'status': status}), content_type="application/json")
        except Exception as e:
            return HttpResponse(force_text(e), status=400)


@require_http_methods(["POST"])
@login_required
def upload_file(request):
    if request.method == 'POST':
        form = TemplateForm(request.POST, request.FILES)
        if form.is_valid():
            filename = form.cleaned_data['attachment']
            contract = form.cleaned_data['contract']
            from openpyxl import load_workbook
            try:
                file_data = filename.read()
                md5_hash = hashlib.md5(file_data).hexdigest()
                wb = load_workbook(filename=ContentFile(file_data))
            except Exception as e:
                return HttpResponse(u'Неверный формат шаблона: %s' % e.message, status=400)
            try:
                ws = wb.active
                vessel_name = force_text(ExcelHelper.get_value(ws, 'VESSEL', True)).upper()
                voyage_name = force_text(ExcelHelper.get_value(ws, 'VOYAGE', True)).upper()               
            except Exception as e:
                return HttpResponse(u'Шаблон заполнен некорректно: %s' % e.message, status=400)

            q = Voyage.objects.filter(name__iexact=voyage_name, vessel__name__iexact=vessel_name)[:1]

            if q:
                voyage = q.get()
            else:
                voyage = Voyage()
                voyage.name = voyage_name
                voyage.user = request.user
                voyage.vessel, created = Vessel.objects.get_or_create(name=vessel_name)  # pylint: disable=W0612
                voyage.save()
            
            order, created = Order.objects.get_or_create(voyage=voyage, contract=contract)  # @UnusedVariable
            
            if not created:
                order_errors = UploadedTemplate.objects.for_user(request.user).filter(
                    status=UploadedTemplate.ERROR).distinct()
                for order_error in order_errors:
                    order_error.deleted = True
                    order_error.save()
                        
            try:
                form.instance = UploadedTemplate.objects.get(order=order, md5_hash=md5_hash)
            except UploadedTemplate.DoesNotExist:
                pass

            template = form.save(commit=False)            
            template.md5_hash = md5_hash
            template.order = order
            template.is_override = True             
            template.user = request.user            
            template.status = UploadedTemplate.REFRESH
            template.attachment = form.cleaned_data['attachment']
            template.save()
            template.services = contract.line.services.values_list('id', flat=True)
            upload_template.delay(template, request.user)
#             upload_template(template, request.user)
            return HttpResponseRedirect(reverse('services'))
        return HttpResponse(u'Неверный формат шаблона: %s' %
                            u''.join([u'%s: %s' % (key, val) for key,
                                      val in form.errors.items()]), status=400)


@job
def upload_template(template, user):
    try:
        draft_service = DraftService(WEB_SERVISES['draft'])
        draft_service.load_draft(template, user)
    except suds.WebFault, f:
        base_error = BaseError()
        base_error.content_object = template
        base_error.type = BaseError.WEBFAULT
        base_error.message = f.fault
        base_error.save()
        template.set_status()        
    except Exception, e:
        logging.exception("Exception")
        base_error = BaseError()
        base_error.content_object = template
        base_error.type = BaseError.UNKNOWN
        base_error.message = e
        base_error.save()
        template.set_status()        
