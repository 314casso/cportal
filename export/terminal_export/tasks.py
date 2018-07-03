from django_rq import job

from export.settings import BASE_RQ_PROC 
from export.local_settings import WEB_SERVISES
from terminal_export.services import TerminalExportService


@job(BASE_RQ_PROC)
def terminal_export_task(user):            
    service = TerminalExportService(WEB_SERVISES['cp'])
    service.get_export(user)      


@job(BASE_RQ_PROC)
def empty_stock_task(user):            
    service = TerminalExportService(WEB_SERVISES['cp'])
    service.get_empty_stock(user)                                            