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
from nutep.models import BaseError
import hashlib
from nutep.services import CRMService, PortalService

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

    def get_context_data(self, **kwargs):
        context = super(BaseView, self).get_context_data(**kwargs)
        manager = self.request.user.managers.first()
        manager.title = u"Ваш менеджер"
        head = manager.head
        head.title = u"Руководитель менеджера" 
        context.update({
            'title': force_unicode('Рускон Онлайн'), 
            'manager': manager,
            'head': head 
        })
        return context


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



 
