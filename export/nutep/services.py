# -*- coding: utf-8 -*-

from django.core.files.base import ContentFile
from export.local_settings import WEB_SERVISES
from nutep.odata import CRM, Portal
from nutep.models import Employee, File
import base64
from suds.cache import NoCache
from suds.client import Client
from django.utils.timezone import now


class WSDLService(object):
    username = None
    password = None
    url = None
    def __init__(self, settings):
        self.set_client(settings)
            
    def set_client(self, settings):
        for key in settings.iterkeys():             
            setattr(self, key, settings.get(key))   
        base64string = base64.encodestring(
            '%s:%s' % (self.username, self.password)).replace('\n', '')
        authenticationHeader = {
            "SOAPAction" : "ActionName",
            "Authorization" : "Basic %s" % base64string
        } 
        self._client = Client(self.url, username=self.username, password=self.password, headers=authenticationHeader, cache=NoCache(), timeout=500)  


class DealService(WSDLService):
    def get_deal_stats(self, user):
        guids = user.profile.ukt_guids 
        for payer in user.profile.payers.all():
            guids.extend(payer.ukt_guids)
                                     
        response = self._client.service.GetDealStats(','.join(set(guids)))         
        return response      


class ReviseService(WSDLService):
    def get_revise(self, user, start_date, end_date):
        if user and user.profile.INN:                                     
            response = self._client.service.GetReport(user.profile.INN, start_date, end_date)
            if hasattr(response, 'Report') and response.Report:
                file_data = response.Report[0].Data                
                filename = u'%s-%s.%s' %  (user.profile.user, 'revise', 'xlsx')
                file_store = File()
                file_store.content_object = user
                file_store.title = filename
                file_store.type = File.REVISE
                file_store.note = u'%s - %s' % (start_date.strftime('%d.%m.%Y'), end_date.strftime('%d.%m.%Y'))                 
                file_store.file.save(filename, ContentFile(base64.b64decode(file_data)))
                return file_store                     
        return response 
    
            
class TrackingService(WSDLService):
    def get_track(self, user):
        if user and user.profile.ukt_guids:                                     
            response = self._client.service.GetRailFreightTracking(user.profile.ukt_guids)
            print response
            if hasattr(response, 'report') and response.report:
                file_data = response.report[0].data                
                filename = u'%s-%s.%s' %  (user.profile.user, 'tracking' , 'xlsx')
                file_store = File()
                file_store.content_object = user
                file_store.title = filename
                file_store.type = File.TRACKING
                file_store.note = u'%s' % (now().strftime('%d.%m.%Y'))                 
                file_store.file.save(filename, ContentFile(base64.b64decode(file_data)))
                return file_store                     
        return response
                

class CRMService(object):
    def __init__(self):
        self.odata = CRM(WEB_SERVISES.get('crm'))
    
    def get_user(self, value):
        return self.odata.get_systemuser(value)
    
    def update_employee(self, employee):
        if employee.crm_id:
            return
        user = self.get_user(employee.domainname)
        for k,v in user.items():
            if hasattr(employee, k):
                setattr(employee, k, v)
        if not employee.head:
            print user['parent_crm_id']
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
        for k,v in user.items():
            if hasattr(employee, k):
                setattr(employee, k, v)
             

        if 'imagedata' in user:
            imagedata = user.get('imagedata') 
            if not imagedata:
                return       
            ext = 'jpg'
            imagedata = ContentFile(base64.b64decode(imagedata), name='avatar.' + ext)
            employee.image.save('avatar.jpg', imagedata)           

