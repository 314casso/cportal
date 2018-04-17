# -*- coding: utf-8 -*-

from __future__ import division

from django.core.cache import cache
from django.utils.timezone import now
from rest_framework import viewsets
from rest_framework.response import Response

import nutep.models
from tracking.serializers import DateQueryTrackingSerializer
from nutep.views import BaseService
from tracking.tasks import tracking_task


class PingTracking(viewsets.ViewSet):
    def list(self, request):
        today = now()
        key = u'last_ping_tracking_%s' % request.user.pk
        if cache.get(key):
            return Response({'job': 'cached'})
        cache.set(key, today, 300)         
        job = tracking_task.delay(request.user)
        return Response({'job': job.id}) 


class TrackingViewSet(viewsets.ModelViewSet):     
    serializer_class = DateQueryTrackingSerializer
    def get_queryset(self):
        q = nutep.models.DateQueryEvent.objects.for_user(
            self.request.user).filter(type=nutep.models.TRACKING)
        q = q.exclude(status__in=(nutep.models.DateQueryEvent.PENDING,))
        return q.order_by('-date')[:1]
        

class TrackingView(BaseService):
    TYPE = nutep.models.TRACKING
    template_name = 'tracking.html'        
    