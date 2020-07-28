# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.contrib import admin
from django.contrib.contenttypes.admin import GenericTabularInline

from inspection.models import Inspection
from nutep.models import File



class FileInline(GenericTabularInline):
    model = File

class InspectionAdmin(admin.ModelAdmin):
    inlines = [
        FileInline,
    ]

admin.site.register(Inspection, InspectionAdmin)
