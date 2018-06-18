# -*- coding: utf-8 -*-

from django.core.files.base import ContentFile

import nutep.models
from nutep.services import BaseEventService


class ContpicsService(BaseEventService):
    def run(self, user, company, start_date, end_date):
        try:            
            event = nutep.models.DateQueryEvent.objects.create(user=user, type=nutep.models.CONTPICS, 
                status=nutep.models.DateQueryEvent.PENDING, company=company)                                             
            if company.ukt_guid:         
                response = self._client.service.getClientPicturesZip(company.ukt_guid, start_date, end_date)                                   
                if hasattr(response, 'data') and response.data:
                    file_data = response.data                
                    filename = u'%s-%s-%s.%s' %  (company, start_date, end_date, 'zip')
                    file_store = event.files.create(title=filename)             
                    file_store.file.save(filename, ContentFile(file_data))
                    event.status = nutep.models.DateQueryEvent.SUCCESS                                                           
            event.status = nutep.models.DateQueryEvent.SUCCESS
            event.save()
        except Exception, e:            
            self.log_event_error(e, event)
