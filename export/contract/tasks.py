from django_rq import job

from contract.services import ContractService, OrderService
from export.local_settings import WEB_SERVISES
from export.settings import BASE_RQ_PROC


@job(BASE_RQ_PROC)
def contract_task(user, company):            
    service = ContractService(WEB_SERVISES['cp'])    
    service.get_contracts(user, company)      


@job(BASE_RQ_PROC)
def contract_files_task(user, company, contract):            
    service = ContractService(WEB_SERVISES['cp'])  
    service.get_files(user, company, contract)      


@job(BASE_RQ_PROC)
def order_list_task(user, company, cfo_guid):            
    service = OrderService(WEB_SERVISES['cp'])
    service.get_order_list(user, company, cfo_guid)          
    

@job(BASE_RQ_PROC)
def order_data_task(user, company, client_order):            
    service = OrderService(WEB_SERVISES['cp'])
    service.get_order_data(user, company, client_order)              