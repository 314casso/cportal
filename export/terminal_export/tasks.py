from django_rq import job

from export.local_settings import WEB_SERVISES
from terminal_export.services import TerminalExportService


@job('default')
def terminal_export_task(user):            
    service = TerminalExportService(WEB_SERVISES['cp'])
    service.get_export(user)      
                                      