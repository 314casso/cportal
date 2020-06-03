from nutep.services import SudsService
import nutep.models
import traceback
from inspection.models import Inspection
from django.core.files.base import ContentFile
import base64


class InspectionService(SudsService):    
    def get_inspections(self, user, company, start_date=None, end_date=None):        
        response = self._client.service.GetInspections(
            company.ukt_guid)
        return response                
    def get_inspection(self, user, company, guid):
        try:            
            event = nutep.models.DateQueryEvent.objects.create(user=user, type=nutep.models.INSPECTION, 
                status=nutep.models.DateQueryEvent.PENDING, company=company)                                             
            
            response = self._client.service.GetInspection(guid)
            if response:
                inspection, created = Inspection.objects.get_or_create(
                  guid=response.guid,
                  container=response.container,
                  date=response.date,
                  number=response.number,                  
                )                
                inspection.company=company
                inspection.event=event
                inspection.save()
                inspection.files.clear()                
                for f in response.attachments:
                    fname = u'%s.%s' % (f.name, f.extension)
                    file_store = inspection.files.create(
                        title=f.name,
                        guid=f.guid, 
                        storage=f.storage,
                        extension=f.extension,
                        )
                    data = base64.b64decode(f.data)
                    file_store.file.save(fname, ContentFile(data))                    
                
            event.status = nutep.models.DateQueryEvent.SUCCESS
            event.save()
            return inspection
        except Exception, e:
            tb = traceback.format_exc()
            self.log_event_error(e, event, tb)
