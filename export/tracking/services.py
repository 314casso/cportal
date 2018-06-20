# -*- coding: utf-8 -*-

from django.core.files.base import ContentFile

import nutep.models
import tracking.models as models
from nutep.services import BaseEventService
from zeep import helpers


class TrackingService(BaseEventService):
    def get_track(self, user):
        try:
            company = user.companies.filter(membership__is_general=True).first()
            event = nutep.models.DateQueryEvent.objects.create(user=user, type=nutep.models.TRACKING, status=nutep.models.DateQueryEvent.PENDING, company=company)                                             
            if company.ukt_guid:         
                response = self._client.service.GetRailFreightTracking(company.ukt_guid)                   
                if hasattr(response, 'report') and response.report:
                    file_data = response.report[0].data                
                    filename = u'%s-%s.%s' %  (company, 'tracking', 'xlsx')
                    file_store = event.files.create(title=filename)             
                    file_store.file.save(filename, ContentFile(file_data))
                    event.status = nutep.models.DateQueryEvent.SUCCESS                                           
                if hasattr(response, 'row') and response.row:
                    for datarow in response.row:
                        tracking = models.RailFreightTracking.objects.create(event=event)
                        mapper = {
                            'container': models.Container,
                            'platform': models.Platform,
                            'raildata': models.RailData,
                            'railtracking': models.RailTracking,
                            'freightdata': models.FreightData,
                            'freighttracking': models.FreightTracking,
                            }
                        for key, model in mapper.items():
                            data_dict = helpers.serialize_object(datarow[key])
                            if data_dict:
                                setattr(tracking, key, model.objects.create(**data_dict))
                        tracking.save()                    
            event.status = nutep.models.DateQueryEvent.SUCCESS
            event.save()
        except Exception, e:            
            self.log_event_error(e, event)  