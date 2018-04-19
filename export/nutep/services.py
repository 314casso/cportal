# -*- coding: utf-8 -*-

import base64

from django.core.files.base import ContentFile
from requests import Session
from requests.auth import HTTPBasicAuth
from zeep import Client, helpers
from zeep.transports import Transport

from export.local_settings import WEB_SERVISES
from nutep.models import (REVISE, TERMINAL_EXPORT, TRACKING, BaseError,
                          DateQueryEvent, Employee)
from nutep.odata import CRM, Portal


class WSDLService(object):
    username = None
    password = None
    url = None
    def __init__(self, settings):
        self.set_client(settings)
            
    def set_client(self, settings):
        for key in settings.iterkeys():             
            setattr(self, key, settings.get(key))   
        
        session = Session()
        session.auth = HTTPBasicAuth(self.username, self.password)         
        self._client = Client(self.url, strict=False, transport=Transport(session=session, timeout=500))  


class DealService(WSDLService):    
    def get_deal_stats(self, user):        
        guids = user.companies.all().values_list('ukt_guid', flat=True)                    
        response = self._client.service.GetDealStats(','.join(guids))                
        return response      


class BaseEventService(WSDLService):    
    def log_event_error(self, e, event, data=None):
        base_error = BaseError()
        base_error.content_object = event
        base_error.type = BaseError.UNKNOWN
        base_error.message = u'%s\n%s' % (e, data)
        base_error.save()  
        event.status = DateQueryEvent.ERROR
        event.save()         
    

class ReviseService(BaseEventService):
    def get_revise(self, user, start_date, end_date):        
        try:            
            company = user.companies.filter(membership__is_payer=True).first()
            if not company:
                raise ValueError('User %s has no payer' % user)
            event = DateQueryEvent.objects.create(user=user, type=REVISE, status=DateQueryEvent.PENDING, company=company)                                             
            if company.ukt_guid:         
                response = self._client.service.GetReport(company.INN, start_date, end_date)
                if response:
                    file_data = response[0].Data                
                    filename = u'%s-%s.%s' %  (company, 'revise', 'xlsx')
                    file_store = event.files.create(title=filename)             
                    file_store.file.save(filename, ContentFile(file_data))
                    event.status = DateQueryEvent.SUCCESS                                         
            event.status = DateQueryEvent.SUCCESS
            event.save()
        except Exception, e:            
            self.log_event_error(e, event) 
     

class CRMService(object):
    def __init__(self):
        self.odata = CRM(WEB_SERVISES.get('crm'))
    
    def get_user(self, value):
        return self.odata.get_systemuser(value)
    
    def update_employee(self, employee):
        if employee.crm_id:
            return
        user = self.get_user(employee.domainname)
        if user:
            for k, v in user.items():
                if hasattr(employee, k):
                    setattr(employee, k, v)
        if not employee.head:            
            head = self.get_user(user['parent_crm_id'])
            if head:
                obj, created = Employee.objects.get_or_create(domainname=head['domainname'])  # @UnusedVariable
                if obj:
                    employee.head = obj  
        

class PortalService(object):  
    def __init__(self):
        self.odata = Portal(WEB_SERVISES.get('portal'))
    
    def get_user(self, domainname, email):
        return self.odata.get_systemuser(domainname, email)
    
    def update_employee(self, employee):
        if employee.portal_id:
            return        
        user = self.get_user(employee.domainname, employee.email)        
        if user:
            for k, v in user.items():
                if hasattr(employee, k):
                    setattr(employee, k, v)

            if 'imagedata' in user:
                imagedata = user.get('imagedata') 
                if not imagedata:
                    return       
                ext = 'jpg'
                imagedata = ContentFile(base64.b64decode(imagedata), name='avatar.' + ext)
                employee.image.save('avatar.jpg', imagedata)           
