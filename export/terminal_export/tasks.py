from django_rq import job

from export.local_settings import WEB_SERVISES
from export.settings import BASE_RQ_PROC
from terminal_export.services import (LineDemurrageService,
                                      TerminalExportService)


@job(BASE_RQ_PROC)
def terminal_export_task(user):            
    service = TerminalExportService(WEB_SERVISES['cp'])
    service.get_export(user)      


@job(BASE_RQ_PROC)
def empty_stock_task(user):            
    service = TerminalExportService(WEB_SERVISES['cp'])
    service.get_empty_stock(user)                                            


@job(BASE_RQ_PROC)
def line_demurrage_task(user):            
    service = LineDemurrageService(WEB_SERVISES['cp'])
    service.get_line_demurrage(user)                                            