# -*- coding: utf-8 -*-

from __future__ import division

from django.core.cache import cache
from django.utils.timezone import now
from rest_framework import viewsets
from rest_framework.response import Response

import nutep.models
from nutep.views import BaseService
from terminal_export.serializers import DateQueryTrackingSerializer
from terminal_export.tasks import terminal_export_task


class PingTerminalExport(viewsets.ViewSet):
    def list(self, request):
        today = now()        
        key = u'last_ping_terminal_export_%s' % request.user.pk
        if cache.get(key):
            return Response({'job': 'cached'})
        cache.set(key, today, 300)
        job = terminal_export_task.delay(request.user)
        return Response({'job': job.id})


class TerminalExportView(BaseService):
    TYPE = nutep.models.TERMINAL_EXPORT
    template_name = 'terminal_export.html'


class TerminalExportViewSet(viewsets.ModelViewSet):
    serializer_class = DateQueryTrackingSerializer

    def get_queryset(self):
        q = nutep.models.DateQueryEvent.objects.for_user(
            self.request.user).filter(type=nutep.models.TERMINAL_EXPORT)
        q = q.exclude(status__in=(nutep.models.DateQueryEvent.PENDING,))
        return q.order_by('-date')[:1]
