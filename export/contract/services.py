# -*- coding: utf-8 -*-

import base64
import json
import traceback

from django.core.files.base import ContentFile

import nutep.models
from contract.models import ClientOrder, Contract, ContractEvent
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


class OrderService(SudsService):     
    def get_order_list(self, user, company, cfo_guid):
        try:
            event = nutep.models.DateQueryEvent.objects.create(user=user, type=nutep.models.ORDER_LIST,
                                                               status=nutep.models.DateQueryEvent.PENDING, company=company)
            if company.ukt_guid:
                response = self._client.service.GetOrderList(company.ukt_guid, cfo_guid)
                if response:
                    for item in json.loads(response):
                        client_order, created = ClientOrder.objects.get_or_create(
                            guid=item['guid'],
                            name=item['name'],                            
                            company=company                            
                        )
                        client_order.data = item['data']
                        client_order.date = item['date']                        
                        client_order.event = event                            
                        client_order.save()
                        if item['contracts']:
                            for contract_dict in item['contracts']:
                                contract, created = Contract.objects.get_or_create(
                                    guid=contract_dict['guid'], 
                                    name=contract_dict['name'],
                                    company=company
                                )  
                                client_order.contracts.add(contract)
                                                
                        if item['data']['files']:
                            for data_dict in item['data']['files']:                                                                
                                file_store, created  = client_order.files.get_or_create(
                                    guid=data_dict['Guid']
                                )
                                file_store.title = data_dict['Name']
                                file_store.storage = u'СделкаСКлиентомПрисоединенныеФайлы'
                                file_store.doc_type = data_dict['Type']
                                file_store.extension = data_dict['Extension']
                                file_store.size = data_dict['Size']
                                file_store.save()

            event.status = nutep.models.DateQueryEvent.SUCCESS
            event.save()
        except Exception, e:
            tb = traceback.format_exc()
            self.log_event_error(e, event, tb)

    def get_order_data(self, user, company, client_order):
        try:
            event = nutep.models.DateQueryEvent.objects.create(user=user, type=nutep.models.ORDER_DATA,
                                                               status=nutep.models.DateQueryEvent.PENDING, company=company)
            
            if client_order and client_order.guid:
                response = self._client.service.GetOrderData(client_order.guid)
                if response:                      
                    client_order.data = json.loads(response)
                    client_order.data_event = event
                    client_order.save()

            event.status = nutep.models.DateQueryEvent.SUCCESS
            event.save()
        except Exception, e:
            tb = traceback.format_exc()
            self.log_event_error(e, event, tb)
