from django_rq import job

from export.settings import BASE_RQ_PROC 
from export.local_settings import WEB_SERVISES
from terminal_export.services import TerminalExportService
from tracking.services import TrackingService


@job(BASE_RQ_PROC)
def tracking_task(user):            
    service = TrackingService(WEB_SERVISES['report'])                        
    service.get_track(user)    
                                      