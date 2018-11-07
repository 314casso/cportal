from django_rq import job

from contract.services import ContractService
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
    