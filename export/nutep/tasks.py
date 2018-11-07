import json

from django_rq import job

from export.settings import BASE_RQ_PROC 
from export.local_settings import WEB_SERVISES 
from nutep.services import DealService, ReviseService, AttachedFileService


@job(BASE_RQ_PROC)
def update_user(user):    
    company = user.companies.filter(membership__is_general=True).first()
    if not company:
        return
    deal_service = DealService(WEB_SERVISES['report'])
    deal_stats = deal_service.get_deal_stats(user)    
    company.details = json.loads(deal_stats)
    company.save()


@job(BASE_RQ_PROC)
def revise_task(user, start_date, end_date):            
    service = ReviseService(WEB_SERVISES['erp'])
    service.get_revise(user, start_date, end_date)                        


def get_attachement(user, guid):
    service = AttachedFileService(WEB_SERVISES['cp'])
    file_store = service.get_attachement(user, guid)
    return file_store
