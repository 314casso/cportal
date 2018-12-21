# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from django.contrib import admin

from contract.models import ClientOrder, Contract, ContractEvent


# Register your models here.

admin.site.register(Contract)
admin.site.register(ContractEvent)
admin.site.register(ClientOrder)
