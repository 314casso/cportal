import json

from django_rq import job

from export.local_settings import WEB_SERVISES
from nutep.services import DealService, ReviseService


@job('default')
def update_user(user):    
    company = user.companies.filter(membership__is_general=True).first()
    if not company:
        return
    deal_service = DealService(WEB_SERVISES['report'])
    deal_stats = deal_service.get_deal_stats(user)    
    company.details = json.loads(deal_stats)
    company.save()

@job('default')
def revise_task(user, start_date, end_date):            
    service = ReviseService(WEB_SERVISES['erp'])
    service.get_revise(user, start_date, end_date)                        
