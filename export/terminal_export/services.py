# -*- coding: utf-8 -*-

import json
import sys
import traceback
from base64 import b64decode

from django.core.files.base import ContentFile
from zeep import helpers

import nutep.models
from nutep.services import BaseEventService
from nutep.utils import set_properties
from terminal_export import models


class TerminalExportService(BaseEventService):
    def get_export(self, user):
        try:
            company = user.companies.filter(
                membership__is_general=True).first()
            event = nutep.models.DateQueryEvent.objects.create(
                user=user, type=nutep.models.TERMINAL_EXPORT, status=nutep.models.DateQueryEvent.PENDING, company=company)
            nomenclature = company.nomencls.filter(is_general=True).first()
            if not nomenclature:
                return
            response = self._client.service.TerminalExport(
                nomenclature.nomenclature.ukt_guid)
            if hasattr(response, 'report') and response.report:
                file_data = response.report[0].data
                filename = u'%s-%s-%s.%s' % (company, 'terminalexport', nomenclature.nomenclature.name, 'xlsx')
                file_store = event.files.create(title=filename)
                file_store.file.save(filename, ContentFile(file_data))
                event.status = nutep.models.DateQueryEvent.SUCCESS
            if hasattr(response, 'row') and response.row:
                for datarow in response.row:
                    terminal_export = models.TerminalExport.objects.create(
                        event=event, rowindex=datarow['rowindex'], nomenclature=nomenclature.nomenclature)
                    container_dict = helpers.serialize_object(datarow['container'])
                    container = models.Container()
                    set_properties(container, container_dict, ['stuffs'])                    
                    container.save()                                        
                    if 'stuffs' in container_dict:
                        for stuff_dict in container_dict['stuffs']:
                            stuffing = models.Stuffing()
                            set_properties(stuffing, stuff_dict)                    
                            stuffing.container = container
                            stuffing.save()
                    terminal_export.container = container
                    terminal_export.save()  
            event.status = nutep.models.DateQueryEvent.SUCCESS
            event.save()
        except Exception, e:
            tb = traceback.format_exc()
            self.log_event_error(e, event, tb)

    def get_empty_stock(self, user):
        try:
            company = user.companies.filter(
                membership__is_general=True).first()
            event = nutep.models.DateQueryEvent.objects.create(
                user=user, type=nutep.models.EMPTY_STOCK, status=nutep.models.DateQueryEvent.PENDING, company=company)
            nomenclature = company.nomencls.filter(is_general=True).first()
            if not nomenclature:
                return
            response = self._client.service.EmptyStock(
                nomenclature.nomenclature.ukt_guid)
            if hasattr(response, 'report') and response.report:
                file_data = response.report[0].data
                filename = u'%s-%s-%s.%s' % (company, 'emptystock', nomenclature.nomenclature.name, 'xlsx')
                file_store = event.files.create(title=filename)
                file_store.file.save(filename, ContentFile(file_data))
                event.status = nutep.models.DateQueryEvent.SUCCESS
            if hasattr(response, 'row') and response.row:
                for datarow in response.row:
                    terminal_export = models.TerminalExport.objects.create(
                        event=event, rowindex=datarow['rowindex'], nomenclature=nomenclature.nomenclature)
                    container_dict = helpers.serialize_object(datarow['container'])
                    container = models.Container()
                    set_properties(container, container_dict, ['stuffs', 'seal', 'emptyweight'])                    
                    container.save()                                                            
                    terminal_export.container = container
                    terminal_export.save()  
            event.status = nutep.models.DateQueryEvent.SUCCESS
            event.save()
        except Exception, e:
            tb = traceback.format_exc()
            self.log_event_error(e, event, tb)

    def get_line_demurrage(self, user):
        try:
            company = user.companies.filter(
                membership__is_general=True).first()
            event = nutep.models.DateQueryEvent.objects.create(
                user=user, type=nutep.models.LINE_DEMURRAGE, status=nutep.models.DateQueryEvent.PENDING, company=company)
            nomenclature = company.nomencls.filter(is_general=True).first()
            if not nomenclature:
                return
            response = self._client.service.LineDemurrage(
                company.ukt_guid,
                nomenclature.nomenclature.ukt_guid)
            if response:
                data = json.loads(response)
                if 'xlsx' in data:                    
                    file_data = b64decode(data['xlsx'])
                    filename = u'%s-%s-%s.%s' % (company, 'linedemurrage', nomenclature.nomenclature.name, 'xlsx')
                    file_store = event.files.create(title=filename)
                    file_store.file.save(filename, ContentFile(file_data))
                    event.status = nutep.models.DateQueryEvent.SUCCESS
                if 'json' in data:                    
                    for datarow in data['json']:
                        line_demurrage = models.LineDemurrage.objects.create(
                            event=event,                             
                            nomenclature=nomenclature.nomenclature                           
                        )
                        set_properties(line_demurrage, datarow, ['container',])                        
                        container = models.Container()
                        set_properties(container, datarow)                    
                        container.number = datarow['container']
                        container.save()                                                            
                        line_demurrage.container = container
                        line_demurrage.save()             
  
            event.status = nutep.models.DateQueryEvent.SUCCESS
            event.save()
        except Exception, e:            
            tb = traceback.format_exc()
            self.log_event_error(e, event, tb)            
