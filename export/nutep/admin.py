from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from django.contrib.auth.models import User

from nutep.models import (BaseError, Container, Contract, Draft, Line,
                          Terminal, UploadedTemplate, UserProfile, Vessel,
                          Voyage, Team, ServiceProvided, Mission, Order)

admin.site.unregister(User)


class UploadedTemplateAdmin(admin.ModelAdmin):
    #list_display = ('attachment', 'history')
    def get_queryset(self, request):
        return UploadedTemplate.all_objects.all()  # pylint: disable=E1101


class VoyageAdmin(admin.ModelAdmin):
    list_display = ('name', 'guid')


class ContractAdmin(admin.ModelAdmin):
    list_display = ('name', )


class ContractInline(admin.TabularInline):
    model = Contract
    extra = 0


class LineAdmin(admin.ModelAdmin):
    list_display = ('name', )
    inlines = [ContractInline, ]
    def get_queryset(self, request):
        return Line.all_objects.all()  # pylint: disable=E1101


class TerminalAdmin(admin.ModelAdmin):
    list_display = ('name', )


class UserProfileInline(admin.StackedInline):
    model = UserProfile
    
class TeamInline(admin.TabularInline):
    model = Team.users.through  # @UndefinedVariable
    extra = 1

class UserProfileAdmin(UserAdmin):
    inlines = [UserProfileInline, TeamInline]

class TeamAdmin(admin.ModelAdmin):
    pass

class ServiceAdmin(admin.ModelAdmin):
    pass

class MissionAdmin(admin.ModelAdmin):
    pass

class OrderAdmin(admin.ModelAdmin):
    def get_queryset(self, request):
        return Order.all_objects.all()  # pylint: disable=E1101  


admin.site.register(User, UserProfileAdmin)
admin.site.register(Voyage, VoyageAdmin)
admin.site.register(Contract, ContractAdmin)
admin.site.register(Line, LineAdmin)
admin.site.register(Terminal, TerminalAdmin)
admin.site.register(Vessel)
admin.site.register(Draft)
admin.site.register(Container)
admin.site.register(BaseError)
admin.site.register(UploadedTemplate, UploadedTemplateAdmin)
admin.site.register(Team, TeamAdmin)
admin.site.register(ServiceProvided, ServiceAdmin)
admin.site.register(Mission, MissionAdmin)
admin.site.register(Order, OrderAdmin)
