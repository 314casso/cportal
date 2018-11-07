# -*- coding: utf-8 -*-

import base64
import json
import traceback

from django.core.files.base import ContentFile

import nutep.models
from contract.models import Contract, ContractEvent
from nutep.services import BaseEventService, SudsService


class ContractService(SudsService):
    def get_contracts(self, user, company):
        try:     
            event = nutep.models.DateQueryEvent.objects.create(user=user, type=nutep.models.CONTRACTS, 
                status=nutep.models.DateQueryEvent.PENDING, company=company)                                                   
            if company.ukt_guid:         
                response = self._client.service.GetContracts(company.ukt_guid)                                   
                if response:                    
                    for item in json.loads(response):                        
                        obj, created = Contract.objects.get_or_create(
                            guid=item['Guid'], 
                            name=item['Name'],
                            company=company
                            )  
            event.status = nutep.models.DateQueryEvent.SUCCESS
            event.save()        
        except Exception, e:
            tb = traceback.format_exc()
            self.log_event_error(e, event, tb)
    
    def get_files(self, user, company, contract):
        try:     
            event = nutep.models.DateQueryEvent.objects.create(user=user, type=nutep.models.CONTRACT_FILES, 
                status=nutep.models.DateQueryEvent.PENDING, company=company)                                                   
            if contract and contract.guid:
                response = self._client.service.GetContractFiles(contract.guid)
                if response:                                        
                    obj, created = ContractEvent.objects.get_or_create(event=event, contract=contract)  
                    for data_dict in json.loads(response):                                               
                        file_store = obj.files.create(
                            title=data_dict['Name'],
                            guid=data_dict['Guid'],
                            storage=u'СделкаСКлиентомПрисоединенныеФайлы',
                            doc_type=data_dict['Type'], 
                            extension=data_dict['Extension'], 
                            size=data_dict['Size']
                            )                      
            event.status = nutep.models.DateQueryEvent.SUCCESS
            event.save()        
        except Exception, e:
            tb = traceback.format_exc()
            self.log_event_error(e, event, tb)



