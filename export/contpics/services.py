# -*- coding: utf-8 -*-

import base64
import traceback

from django.core.files.base import ContentFile

import nutep.models
from nutep.services import SudsService


class ContpicsService(SudsService):
    def run(self, user, company, start_date, end_date):
        try:            
            event = nutep.models.DateQueryEvent.objects.create(user=user, type=nutep.models.CONTPICS, 
                status=nutep.models.DateQueryEvent.PENDING, company=company)                                             
            if company.ukt_guid:         
                response = self._client.service.getClientPicturesZip(company.ukt_guid, start_date, end_date)                                   
                if response:
                    for f in response.pictures:
                        file_data = base64.b64decode(f.data)
                        filename = u'%s-%s-%s.%s' %  (company, start_date, end_date, 'zip')
                        file_store = event.files.create(title=filename)             
                        file_store.file.save(filename, ContentFile(file_data))                    
            event.status = nutep.models.DateQueryEvent.SUCCESS
            event.save()
        except Exception, e:
            tb = traceback.format_exc()
            self.log_event_error(e, event, tb)
