from django_rq import job

from contpics.services import ContpicsService
from export.local_settings import WEB_SERVISES
from export.settings import BASE_RQ_PROC

SERVICE_NAME = 'cp_dc'

@job(BASE_RQ_PROC)
def contpics_task(user, company, start_date, end_date):            
    service = ContpicsService(WEB_SERVISES[SERVICE_NAME])    
    service.run(user, company, start_date, end_date)      
                                      