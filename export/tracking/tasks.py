from django_rq import job

from export.local_settings import WEB_SERVISES
from terminal_export.services import TerminalExportService
from tracking.services import TrackingService


@job('default')
def tracking_task(user):            
    service = TrackingService(WEB_SERVISES['report'])                        
    service.get_track(user)    
                                      