# -*- coding: utf-8 -*-

import base64

from django.apps import apps
from django.contrib.auth.models import User
from django.core.files.base import ContentFile
from suds.cache import NoCache
from suds.client import Client

from nutep.models import (BaseError, Container, Contract, Draft, File, Line,
                          Mission, Readiness, UploadedTemplate, Voyage, Order)
from django.utils.encoding import force_text


class BaseService(object):
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
        self._client = Client(self.url, headers=authenticationHeader, cache=NoCache(), timeout=500)        


class MissionService(BaseService):
    def get_mission_xlsx(self, pk, user): 
        mission = Mission.objects.get(pk=pk) # pylint: disable=E1101                
        response = self._client.service.GetMissionXlsx(mission.guid)
         
        if hasattr(response, 'attachments') and response.attachments:
            mission.xlsx_files().delete()
            for xml_attachment in response.attachments.attachment:
                filename = u'%s.%s' %  (mission, xml_attachment.extension)
                file_store = File()
                file_store.content_object = mission
                file_store.title = filename 
                file_store.note = u"%s" % xml_attachment.note if xml_attachment.note else None 
                file_store.file.save(filename, ContentFile(base64.b64decode(xml_attachment.data)))
                return file_store
    

class LoadingListService(BaseService):
    def get_loading_list(self, pk, user): 
        template = UploadedTemplate.objects.get(pk=pk) # pylint: disable=E1101
        template.user = user        
        response = self._client.service.GetLL(template.order.pk, u'Общий')
        
        if hasattr(response, 'attachments') and response.attachments:
            template.order.files.all().delete()
            for xml_attachment in response.attachments.attachment:
                filename = u'%s.%s.%s' %  (template.order.voyage.vessel, template.order.voyage, xml_attachment.extension)
                file_store = File()
                file_store.content_object = template.order
                file_store.title = filename 
                file_store.note = u"%s" % xml_attachment.note if xml_attachment.note else None 
                file_store.file.save(filename, ContentFile(base64.b64decode(xml_attachment.data)))
        if template.order.files:
            return template.order.files.first()               


class DraftService(BaseService):       
    def update_voyage(self, template, xml_voyage):
        vessel = self.get_value('Vessel', xml_voyage.vessel) 
        value = template.voyage
        is_diff = False
        if not value.vessel == vessel:
            value.vessel = vessel
            is_diff = True

        fields = ['name', 'eta', 'guid', 'flag']
        for field in fields:  
            if not getattr(value, field) == getattr(xml_voyage, field):
                setattr(value, field, getattr(xml_voyage, field))
                is_diff = True
        
        if is_diff is True:
            value.save() 

    def get_voyage(self, xml_voyage):
        vessel = self.get_value('Vessel', xml_voyage.vessel)        
        model = Voyage
        xml_value = xml_voyage
        try:
            value = model.objects.get(guid=xml_value.guid,)
        except model.DoesNotExist:
            value = None
        if not value:
            q = model.objects.filter(name=xml_value.name, vessel=vessel, guid__isnull=True)
            if q:
                value = q.first()
                value.guid = xml_value.guid        
                value.save()       
        if not value:                      
            value = model.objects.create(guid=xml_value.guid,)
            value.name = xml_value.name
            value.vessel = vessel
            value.eta = xml_value.eta
            value.guid = xml_value.guid        
            value.save()        
        return value
    
    def get_line(self, xml_line):         
        line, created = Line.objects.get_or_create(guid=xml_line.guid,)  # pylint: disable=E1101,W0612
        line.name = xml_line.name        
        line.guid = xml_line.guid
        line.save()        
        return line
    
    def get_value(self, model_name, xml_value):
        model = apps.get_model(app_label='nutep', model_name=model_name)
        try:
            value = model.objects.get(guid=xml_value.guid,)
        except model.DoesNotExist:
            value = None
        if not value:
            q = model.objects.filter(name=xml_value.name, guid__isnull=True)
            if q:
                value = q.first()
                value.guid = xml_value.guid        
                value.save()       
        if not value:                      
            value = model.objects.create(guid=xml_value.guid,)
            value.name = xml_value.name
            value.guid = xml_value.guid        
            value.save()        
        return value
    
    def get_vessel(self, xml_vessel):             
        return self.get_value('Vessel', xml_vessel)
    
    def get_contract(self, xml_contract):         
        contract, created = Contract.objects.get_or_create(guid=xml_contract.guid,)  # pylint: disable=E1101,W0612
        contract.name = xml_contract.name
        contract.guid = xml_contract.guid        
        contract.save()        
        return contract

    def load_draft(self, template, user):
        xml_template = self._client.factory.create('ns0:Template')
        xml_template.id = template.order.id
        xml_template.userguid = user.profile.guid
        xml_template.contractguid = template.contract.guid
        xml_template.override = template.is_override         
        xml_template.data = template.attachment.read().encode('base64')
                                
        xml_services = self._client.factory.create('ns0:Services')
        
        services = []  
        for service in template.services.all():
            xml_service = self._client.factory.create('ns0:Service')     
            xml_service.id = service.service
            services.append(xml_service)                    
        xml_services.service = services
        xml_template.services = xml_services 
        
                                
        response = self._client.service.LoadDraft(xml_template)                
        self.parse_response(response, template)
        return response
                        
    def update_status(self, pk, user): 
        template = UploadedTemplate.objects.get(pk=pk) # pylint: disable=E1101
        template.user = user 
        #if template.errors.all():
        #    raise Exception(u"Шаблон содержит ошибки, обновление новозможно")
        response = self._client.service.GetStatus(template.order.pk)      
        self.parse_response(response, template)
        return response
    
    def parse_errors(self, response, template):        
        if not response.errors:
            return
        fields = ['code', 'error', 'message']
        for xml_error in response.errors.error:                  
            base_error = BaseError()
            for field in fields:
                value = u'%s' % xml_error[field] if field in xml_error else None                        
                setattr(base_error, field, value)                
            base_error.content_object = template
            base_error.type = BaseError.XML
            base_error.save()                

    def parse_draft(self, response, template):        
        if not response.drafts: 
            return
        for xml_draft in response.drafts.draft:            
            draft = Draft()
            fields = ['name', 'guid', 'date', 'shipper', 'consignee', 'finalDestination',
                        'POD', 'POL', 'finstatus', 'status', 'poruchenie', 'poruchenieNums', 'notify']
            for field in fields:
                value = u'%s' % xml_draft[field] if xml_draft[field] else xml_draft[field]                        
                setattr(draft, field, value)                
            draft.user = User.objects.get(profile__guid=xml_draft.userguid)                                
            draft.voyage = self.get_voyage(xml_draft.voyage) 
            draft.line = self.get_line(xml_draft.line)
            draft.order = template.order               
            draft.save()
            
            self.parse_container(xml_draft, draft)
            self.parse_readiness(xml_draft, draft)
            self.parse_missions(xml_draft, draft)        

    def parse_container(self, xml_draft, draft):        
        fields = ['name', 'SOC', 'size', 'type', 'seal', 'cargo',
                          'netto', 'gross', 'tare', 'package', 'quantity']
        if not xml_draft.containers:
            return
        for xml_container in xml_draft.containers.container:
            container = Container()
            for field in fields:
                value = u'%s' % xml_container[field] if xml_container[field] else xml_container[field]
                setattr(container, field, value)
            container.line = self.get_line(xml_container.line)
            container.draft = draft
            container.save()            

    def parse_readiness(self, xml_draft, draft):
        fields = ['size', 'type', 'ordered', 'done', ]
        if not xml_draft.readiness:
            return
        for xml_readiness in xml_draft.readiness.row:
            readiness = Readiness()
            for field in fields:                    
                setattr(readiness, field, xml_readiness[field])                
            readiness.draft = draft
            readiness.save()  

    def parse_missions(self, xml_draft, draft): 
        if not xml_draft.missions:
            return
        fields = ['name', 'guid', 'reception_date', 'issue_date']                
        for xml_mission in xml_draft.missions.mission:
            mission = Mission()
            for field in fields: 
                if hasattr(xml_mission, field):                                        
                    setattr(mission, field, xml_mission[field])                                            
            mission.draft = draft
            mission.save()
            if hasattr(xml_mission, 'attachments') and xml_mission.attachments:
                for xml_attachment in xml_mission.attachments.attachment:
                    filename = '%s.%s' %  (xml_attachment.name, xml_attachment.extension)
                    file_store = File()
                    file_store.content_object = mission
                    file_store.title = filename
                    file_store.note = u"%s" % xml_attachment.note if xml_attachment.note else None 
                    file_store.file.save(filename, ContentFile(base64.b64decode(xml_attachment.data)))        

    def parse_response(self, response, template):        
        self.delete_data(template)    
        self.parse_errors(response, template)                
        if template.errors.all():
            template.set_status()
            return response                
        self.update_voyage(template, response.voyage)       
        template.xml_response = response
        template.save()  
        self.parse_draft(response, template)        
        template.set_status()
            
    def delete_data(self, template):        
        drafts = Draft.objects.filter(order=template.order)
        drafts.delete()
        template.errors.all().delete()


class TemplateException(Exception):
    pass   


class ExcelHelper(object):    
    @staticmethod            
    def get_value(ws, col_name, required=False):
        cell = ExcelHelper.get_cell(ws, col_name)
        value = ExcelHelper.get_cell_value(ws, cell)
        if required and not value:
            raise TemplateException(u'Столбец %s не может быть пустым' % col_name) 
        return value
            
    @staticmethod
    def get_cell(ws, col_name):        
        for row in ws.iter_rows(min_row=1, max_col=ws.max_column, max_row=ws.max_row):               
            for cell in row:
                cval = u'%s' % cell.value
                if cell.value and cval.upper() == col_name.upper():
                    return cell
        raise TemplateException(u'Столбец %s не найден' % col_name) 
        
    @staticmethod            
    def get_cell_value(ws, cell):
        rng = "%s%s:%s%s" % (cell.column, int(cell.row) + 1,
                             cell.column, int(cell.row) + 1)
        result = set() 
        for row in ws.iter_rows(rng):
            result.add(row[0].value)            
        if len(result) == 1:
            return result.pop()
        elif len(result) == 0:
            raise TemplateException(u'Столбец %s не заполнен' % cell.value)               
        else:
            raise TemplateException(u'Столбец %s содержит более одного рейса %s' % (cell.value, u','.join(result)))  
