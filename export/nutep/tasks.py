from django_rq import job
from nutep.services import DealService
from export.local_settings import WEB_SERVISES
import json


@job('default')
def update_user(user):
    print "DO UPDATE"
    company = user.companies.filter(membership__is_general=True).first()
    if not company:
        return
    deal_service = DealService(WEB_SERVISES['report'])
    deal_stats = deal_service.get_deal_stats(user)    
    company.details = json.loads(deal_stats)
    company.save()
    print company.details